# Patterns

| Pattern | Where it lives | Key classes/files | Why this choice |
| --- | --- | --- | --- |
| Strategy | Pricing pipeline | `apps/pricing/services.py`, `apps/pricing/strategies.py` | Keeps pricing extensible by chaining independent strategies (base price, duration discounts, depreciation, seasonal rules) so new pricing adjustments can be introduced without rewriting the service. |
| State | Booking lifecycle | `apps/bookings/state.py` | Encapsulates booking status rules and enforces allowed transitions while synchronizing car availability, preventing invalid state changes. |
| Observer | Domain event bus | `apps/common/event_bus.py`, handlers triggered in `apps/bookings/state.py` and `apps/bookings/services.py` | Decouples side effects (notifications, ledger hooks) from core actions like confirmation, return, and fines. |
| Factory | Payment providers | `apps/payments/factory.py`, consumed by `apps/payments/services.py` | Allows swapping/mock payment providers without changing payment logic. |
| Builder | Invoice aggregation | `apps/bookings/invoice_builder.py` | Collects rental charges, seasonal adjustments, and fines before persisting a single invoice, keeping invoice assembly coherent and testable. |
