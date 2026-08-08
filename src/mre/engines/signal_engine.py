"""Signal Engine (ENG-003, ARC-006 §7.4)."""

from __future__ import annotations

from collections.abc import Sequence

from mre.models.event import Event
from mre.models.signal import Signal
from mre.models.signal_rule import SignalRule, payload_matches


def combine(events: Sequence[Event], signal_definition: Sequence[SignalRule]) -> tuple[Signal, ...]:
    """Combine Events into Signals according to the signal definition.

    Per rule: each trigger Event must be followed, within ``window``
    candle references, by the earliest confirmation Event of every
    required type. The resulting Signal timestamp is the latest of its
    constituent Events (FND-009 §13.5).

    Raises ValueError if the definition is empty or an Event reference
    is not an integer (required for window semantics).
    """
    if not signal_definition:
        raise ValueError("signal definition is required")

    sorted_events = sorted(events, key=lambda e: (e.timestamp, e.event_type, _ref(e)))

    signals: list[Signal] = []
    for rule in signal_definition:
        triggers = [
            e for e in sorted_events
            if e.event_type == rule.trigger and payload_matches(e.payload, rule.trigger_payload)
        ]
        confirmations_by_type = {
            event_type: [e for e in sorted_events if e.event_type == event_type]
            for event_type in rule.confirmations
        }

        for trigger in triggers:
            trigger_ref = _ref(trigger)
            selected: list[Event] = [trigger]
            valid = True
            for event_type in rule.confirmations:
                candidate = None
                for e in confirmations_by_type[event_type]:
                    if _ref(e) > trigger_ref and _ref(e) - trigger_ref <= rule.window:
                        candidate = e
                        break
                if candidate is None:
                    valid = False
                    break
                selected.append(candidate)
            if not valid:
                continue

            selected.sort(key=lambda e: (e.timestamp, e.event_type, _ref(e)))
            signals.append(
                Signal(
                    signal_type=rule.signal_type,
                    timestamp=selected[-1].timestamp,
                    events=tuple(selected),
                    confirmation=True,
                    source_strategy=rule.source_strategy,
                    experiment_id=trigger.experiment_id,
                )
            )

    return tuple(signals)


def _ref(event: Event) -> int:
    if not isinstance(event.reference, int):
        raise ValueError(f"event reference must be an int, got {event.reference!r}")
    return event.reference
