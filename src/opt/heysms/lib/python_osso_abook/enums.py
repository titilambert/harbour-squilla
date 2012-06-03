


class OssoABookAggregatorState:
    OSSO_ABOOK_AGGREGATOR_PENDING       = 0
    OSSO_ABOOK_AGGREGATOR_RUNNING       = 1 << 0
    OSSO_ABOOK_AGGREGATOR_MASTERS_READY = 1 << 1
    OSSO_ABOOK_AGGREGATOR_ROSTERS_READY = 1 << 2
    OSSO_ABOOK_AGGREGATOR_READY         = OSSO_ABOOK_AGGREGATOR_MASTERS_READY | OSSO_ABOOK_AGGREGATOR_ROSTERS_READY
    
def EnumResult(enum, value):
    if value in vars(enum).values():
        return value
    raise ValueError("%r not in %s" %(value, enum))
