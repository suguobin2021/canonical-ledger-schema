from datetime import datetime

class ValidationError(ValueError):
    pass

def _time(value, field):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ValidationError(field + " must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValidationError(field + " must include timezone")
    return parsed

def validate_ledger(document):
    if document.get("schema_version") != "0.1.0":
        raise ValidationError("unsupported schema_version")
    trades = document.get("trades")
    if not isinstance(trades, list):
        raise ValidationError("trades must be a list")
    seen = set()
    for i, trade in enumerate(trades):
        required = ("trade_id","instrument","side","status","signal_time","entry_time","entry_price")
        for field in required:
            if field not in trade:
                raise ValidationError("required field missing: " + field)
        tid = trade["trade_id"]
        if not isinstance(tid, str) or not tid or tid in seen:
            raise ValidationError("trade_id must be unique and non-empty")
        seen.add(tid)
        if trade["side"] not in ("long","short"):
            raise ValidationError("invalid side")
        if trade["status"] not in ("open","settled","censored"):
            raise ValidationError("invalid status")
        if not isinstance(trade["entry_price"], (int,float)) or trade["entry_price"] <= 0:
            raise ValidationError("entry_price must be positive")
        signal = _time(trade["signal_time"], "signal_time")
        entry = _time(trade["entry_time"], "entry_time")
        if entry < signal:
            raise ValidationError("entry precedes signal")
        exit_time, exit_price = trade.get("exit_time"), trade.get("exit_price")
        if trade["status"] == "settled" and (exit_time is None or exit_price is None):
            raise ValidationError("settled trade requires exit_time and exit_price")
        if exit_time is not None and _time(exit_time, "exit_time") < entry:
            raise ValidationError("exit precedes entry")
        if exit_price is not None and (not isinstance(exit_price,(int,float)) or exit_price <= 0):
            raise ValidationError("exit_price must be positive")
        cost = trade.get("cost_return")
        if cost is not None and (not isinstance(cost,(int,float)) or cost < 0):
            raise ValidationError("cost_return must be non-negative")
        gross, net = trade.get("gross_return"), trade.get("net_return")
        if gross is not None and cost is not None and net is not None and abs((gross-cost)-net) > 1e-12:
            raise ValidationError("net_return identity failed")
