
import customtkinter as ctk
from typing import Any, Dict, Optional, Tuple


def ellipsize_for_width(text, avail_px, tkfont):
    if tkfont.measure(text) <= avail_px:
        return text
    ell = "…"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi) // 2
        candidate = text[:mid].rstrip() + ell
        if tkfont.measure(candidate) <= avail_px:
            lo = mid + 1
        else:
            hi = mid
    return text[:max(0, lo-1)].rstrip() + ell

def create_button(
        master,
        text: str,
        width: int = 100,
        height: int = 35,
        font: tuple = ("Poppins", 14),
        command=None,
        **kwargs
) -> ctk.CTkButton:
    """
    Crée un widget button
    """
    return ctk.CTkButton(
        master,
        text=text,
        width=width,
        height=height,
        font=font,
        command=command,
        **kwargs
    )

def create_label(
        master,
        text: str,
        font: tuple = ("Poppins", 13),
        **kwargs
) -> ctk.CTkLabel:
    """
    Crée un widget label
    """
    return ctk.CTkLabel(
        master,
        text=text,
        font=font,
        **kwargs
    )

def create_entry(
        master,
        width: int = 300,
        placeholder_text: Optional[str] = None,
        font: tuple = ("Poppins", 12),
        **kwargs
) -> ctk.CTkEntry:
    """
    Crée un widget entry
    """
    kwargs = {**kwargs}
    if placeholder_text is not None:
        kwargs["placeholder_text"] = placeholder_text
    return ctk.CTkEntry(
        master,
        width=width,
        font=font,
        **kwargs
    )

def create_form_row(
        master,
        label_text: str,
        row: int,
        column_label: int = 0,
        column_entry: int = 1,
        label_kwargs: Optional[Dict[str, Any]] = None,
        entry_kwargs: Optional[Dict[str, Any]] = None,
        pady: int = 8,
        padx_label: int = 30,
        padx_entry: int = 50,
        sticky_label: str = "e",
        sticky_entry: str = "w"
) -> Tuple[ctk.CTkLabel, ctk.CTkEntry]:
    label = create_label(master, text=label_text, **(label_kwargs or {}))
    entry = create_entry(master, **(entry_kwargs or {}))
    label.grid(row=row, column=column_label, pady=pady, padx=padx_label, sticky=sticky_label)
    entry.grid(row=row, column=column_entry, pady=pady, padx=padx_entry, sticky=sticky_entry)
    return label, entry