def reset_requested_for_page(reset_requested: int, page_no: int) -> int:
    """Apply a requested vector reset only when indexing starts at page one."""

    return int(bool(reset_requested) and page_no == 1)
