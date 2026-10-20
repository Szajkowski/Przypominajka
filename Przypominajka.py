import sys
import os
import json
from datetime import datetime
from typing import Any, Dict, List
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QLineEdit, QRadioButton,
    QCalendarWidget, QDialog, QMessageBox, QFrame, QComboBox, QToolButton
)
from PyQt6.QtGui import QIcon, QTextCharFormat, QColor
from PyQt6.QtCore import Qt

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "przypominajka_dane.json")

MONTH_NAMES = [
    "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
]

# --- UNIWERSALNY SZABLON STYLU (QSS) ---

BASE_QSS_TEMPLATE = """
    QWidget {{
        background-color: {bg_main};
        color: {text_main};
        font-size: 13px;
    }}
    QLabel#Header {{
        font-size: 18px;
        font-weight: bold;
        color: {header};
        margin: 0px;
        padding: 0px;
    }}
    QLabel#SubHeader {{
        font-size: 15px;
        font-weight: bold;
        color: {text_sub};
        margin: 0px;
        padding: 0px;
    }}
    QListWidget#TodayList {{
        background-color: {bg_card};
        border: 2px solid {accent};
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        color: {text_main};
    }}
    QListWidget#TodayList::item:hover {{
        background-color: {bg_hover};
        border-radius: 6px;
    }}
    QListWidget#TodayList::item:selected {{
        background-color: {accent};
        color: {btn_text};
        border-radius: 6px;
    }}
    QListWidget, QLineEdit {{
        background-color: {bg_card};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 6px;
        color: {text_main};
        selection-background-color: {accent};
        selection-color: {btn_text};
    }}
    QListWidget::item:hover {{
        background-color: {bg_hover};
        border-radius: 4px;
    }}
    QListWidget::item:selected {{
        background-color: {accent};
        color: {btn_text};
        border-radius: 4px;
    }}
    QPushButton {{
        background-color: {btn_bg};
        color: {btn_text};
        border: none;
        border-radius: 6px;
        padding: 8px 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {btn_hover};
        color: {btn_hover_text};
    }}
    QPushButton#ThemeToggleBtn {{
        background-color: {bg_card};
        color: {text_main};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 14px;
    }}
    QPushButton#ThemeToggleBtn:hover {{
        background-color: {bg_hover};
        border-color: {accent};
    }}
    QRadioButton {{
        color: {text_main};
        spacing: 6px;
    }}
    /* Wygląd Selectora Motywów */
    QComboBox {{
        background-color: {bg_card};
        color: {text_main};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 5px 10px;
        font-weight: 500;
    }}
    QComboBox:hover {{
        border-color: {accent};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 18px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {bg_card};
        color: {text_main};
        border: 1px solid {border};
        border-radius: 6px;
        selection-background-color: {accent};
        selection-color: {btn_text};
        padding: 4px;
        outline: none;
    }}

    QCalendarWidget QWidget {{
        background-color: {bg_card};
        color: {text_main};
    }}
    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: {bg_card};
        border-bottom: 1px solid {border};
    }}
    QCalendarWidget QToolButton#qt_calendar_monthbutton,
    QCalendarWidget QToolButton#qt_calendar_yearbutton {{
        color: {header};
        background-color: {bg_card};
        border-radius: 4px;
        padding: 4px 8px;
        font-weight: bold;
        font-size: 14px;
    }}
    QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator {{
        image: none;
        width: 0px;
    }}
    QCalendarWidget QToolButton#qt_calendar_monthbutton:hover,
    QCalendarWidget QToolButton#qt_calendar_yearbutton:hover {{
        background-color: {bg_hover};
    }}
    QCalendarWidget QToolButton#qt_calendar_prevmonth,
    QCalendarWidget QToolButton#qt_calendar_nextmonth {{
        color: {header};
        background-color: {bg_card};
        border-radius: 4px;
        font-size: 16px;
        font-weight: 900;
        min-width: 28px;
        min-height: 24px;
    }}
    QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
    QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {{
        background-color: {bg_hover};
    }}
    QCalendarWidget QTableView {{
        background-color: {bg_card};
        color: {text_main};
        selection-background-color: {accent};
        selection-color: {btn_text};
        gridline-color: {border};
        border: 1px solid {border};
    }}
    QCalendarWidget QHeaderView {{
        background-color: {bg_card};
        border: none;
    }}
    QCalendarWidget QHeaderView::section {{
        background-color: {accent};
        color: {btn_text};
        border: none;
        border-bottom: 1px solid {border};
        padding: 4px;
        font-weight: bold;
    }}
"""

# --- NEUTRALNE TŁA I TEKSTY (DARK vs LIGHT) ---

BASE_NEUTRALS = {
    "dark": {
        "bg_main": "#18181b",
        "bg_card": "#27272a",
        "bg_hover": "#3f3f46",
        "border": "#3f3f46",
        "text_main": "#f4f4f5",
        "text_sub": "#a1a1aa",
    },
    "light": {
        "bg_main": "#f1f3f5",
        "bg_card": "#ffffff",
        "bg_hover": "#e9ecef",
        "border": "#d1d5db",
        "text_main": "#1f2937",
        "text_sub": "#1f2937",
    }
}

# --- AKCENTY KOLORYSTYCZNE ---

THEME_ACCENTS: Dict[str, Dict[str, Dict[str, str]]] = {
    "Fioletowy": {
        "dark": {
            "header": "#c084fc",
            "accent": "#7c3aed",
            "btn_bg": "#7c3aed",
            "btn_hover": "#9333ea",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#6d28d9",
            "accent": "#7c3aed",
            "btn_bg": "#7c3aed",
            "btn_hover": "#6d28d9",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    },
    "Czerwony": {
        "dark": {
            "header": "#f87171",
            "accent": "#dc2626",
            "btn_bg": "#dc2626",
            "btn_hover": "#ef4444",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#b91c1c",
            "accent": "#dc2626",
            "btn_bg": "#dc2626",
            "btn_hover": "#b91c1c",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    },
    "Niebieski": {
        "dark": {
            "header": "#60a5fa",
            "accent": "#2563eb",
            "btn_bg": "#2563eb",
            "btn_hover": "#3b82f6",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#1d4ed8",
            "accent": "#2563eb",
            "btn_bg": "#2563eb",
            "btn_hover": "#1d4ed8",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    },
    "Zielony": {
        "dark": {
            "header": "#34d399",
            "accent": "#059669",
            "btn_bg": "#059669",
            "btn_hover": "#10b981",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#047857",
            "accent": "#059669",
            "btn_bg": "#059669",
            "btn_hover": "#047857",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    },
    "Różowy": {
        "dark": {
            "header": "#f472b6",
            "accent": "#db2777",
            "btn_bg": "#db2777",
            "btn_hover": "#ec4899",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#be185d",
            "accent": "#db2777",
            "btn_bg": "#db2777",
            "btn_hover": "#be185d",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    },
    "Pomarańczowy": {
        "dark": {
            "header": "#fb923c",
            "accent": "#ea580c",
            "btn_bg": "#ea580c",
            "btn_hover": "#f97316",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#c2410c",
            "accent": "#ea580c",
            "btn_bg": "#ea580c",
            "btn_hover": "#c2410c",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    },
    "Żółty": {
        "dark": {
            "header": "#ff8906",
            "accent": "#ff8906",
            "btn_bg": "#ff8906",
            "btn_hover": "#f25f4c",
            "btn_text": "#0f0e17",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#b45309",
            "accent": "#d97706",
            "btn_bg": "#d97706",
            "btn_hover": "#b45309",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    },
    "Szary": {
        "dark": {
            "header": "#a1a1aa",
            "accent": "#52525b",
            "btn_bg": "#3f3f46",
            "btn_hover": "#52525b",
            "btn_text": "#f4f4f5",
            "btn_hover_text": "#ffffff"
        },
        "light": {
            "header": "#27272a",
            "accent": "#52525b",
            "btn_bg": "#3f3f46",
            "btn_hover": "#27272a",
            "btn_text": "#ffffff",
            "btn_hover_text": "#ffffff"
        }
    }
}


def get_theme_qss(theme_name: str, is_dark: bool) -> str:
    mode_key = "dark" if is_dark else "light"
    neutrals = BASE_NEUTRALS[mode_key]

    accents_dict = THEME_ACCENTS.get(theme_name, THEME_ACCENTS["Fioletowy"])
    accents = accents_dict[mode_key]

    combined = {**neutrals, **accents}
    return BASE_QSS_TEMPLATE.format(**combined)


def load_data() -> Dict[str, Any]:
    default_structure: Dict[str, Any] = {"theme": "Fioletowy", "dark_mode": True, "events": []}
    if not os.path.exists(DATA_FILE):
        return default_structure
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
            if isinstance(content, dict):
                if "dark_mode" not in content:
                    content["dark_mode"] = True
                return content
            return default_structure
    except (json.JSONDecodeError, OSError):
        return default_structure


def get_events(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_events = data.get("events")
    if isinstance(raw_events, list):
        return [ev for ev in raw_events if isinstance(ev, dict)]
    return []


def save_data(data: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def format_date_to_polish(date_str: str) -> str:
    parts = date_str.split("-")
    try:
        if len(parts) == 3:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            if 1 <= month <= 12:
                return f"{day} {MONTH_NAMES[month - 1]} {year}"
        elif len(parts) == 2:
            month, day = int(parts[0]), int(parts[1])
            if 1 <= month <= 12:
                return f"{day} {MONTH_NAMES[month - 1]}"
    except ValueError:
        pass
    return date_str


def get_sort_key(ev: Dict[str, Any]) -> tuple:
    date_str = str(ev.get("date", ""))
    parts = date_str.split("-")
    try:
        if len(parts) == 3:
            return 0, int(parts[0]), int(parts[1]), int(parts[2])
        elif len(parts) == 2:
            return 1, 0, int(parts[0]), int(parts[1])
    except ValueError:
        pass
    return 9, 9, 9, 9


class ManagerDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Menedżer wydarzeń")
        self.setMinimumSize(460, 650)

        data = load_data()
        self.is_dark_mode = bool(data.get("dark_mode", True))
        self.current_theme = str(data.get("theme", "Fioletowy"))
        mode_key = "dark" if self.is_dark_mode else "light"

        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>Wybierz datę:</b>"))
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumHeight(280)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        accent_color = THEME_ACCENTS.get(self.current_theme, THEME_ACCENTS["Fioletowy"])[mode_key]["accent"]
        text_on_accent = THEME_ACCENTS.get(self.current_theme, THEME_ACCENTS["Fioletowy"])[mode_key]["btn_text"]

        fmt_header = QTextCharFormat()
        fmt_header.setBackground(QColor(accent_color))
        fmt_header.setForeground(QColor(text_on_accent))
        self.calendar.setHeaderTextFormat(fmt_header)

        # Wyłączenie irytującej domyślnej czerwieni weekendów (poprzez nakładanie pustego formatu).
        # Qt inteligentnie połączy to w locie z fmt_header powyżej, więc
        # dni u góry będą jednolicie kolorowe, a same cyfry normalne, bez błędów dat
        clean_fmt = QTextCharFormat()
        self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, clean_fmt)
        self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, clean_fmt)

        prev_btn = self.calendar.findChild(QToolButton, "qt_calendar_prevmonth")
        next_btn = self.calendar.findChild(QToolButton, "qt_calendar_nextmonth")

        if isinstance(prev_btn, QToolButton):
            prev_btn.setIcon(QIcon())
            prev_btn.setText("◀")
        if isinstance(next_btn, QToolButton):
            next_btn.setIcon(QIcon())
            next_btn.setText("▶")

        layout.addWidget(self.calendar)

        layout.addWidget(QLabel("<b>Treść wydarzenia:</b>"))
        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("np. Urodziny Mamy / Dentysta 15:00")
        layout.addWidget(self.event_input)

        layout.addWidget(QLabel("<b>Typ wydarzenia:</b>"))
        self.radio_annual = QRadioButton("Powtarzaj co rok (np. urodziny)")
        self.radio_once = QRadioButton("Jednorazowe (usuń po pokazaniu)")
        self.radio_single = QRadioButton("Jednorazowe (nie usuwaj)")

        self.radio_annual.setChecked(True)

        layout.addWidget(self.radio_annual)
        layout.addWidget(self.radio_once)
        layout.addWidget(self.radio_single)

        self.add_btn = QPushButton("Dodaj wydarzenie")
        self.add_btn.clicked.connect(self.add_event)
        layout.addWidget(self.add_btn)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        layout.addWidget(QLabel("<b>Zapisane wydarzenia:</b>"))
        self.events_list = QListWidget()
        layout.addWidget(self.events_list)

        self.del_btn = QPushButton("Usuń zaznaczone")
        self.del_btn.clicked.connect(self.delete_event)
        layout.addWidget(self.del_btn)

        self.setLayout(layout)
        self.refresh_list()

    def refresh_list(self) -> None:
        self.events_list.clear()
        data = load_data()
        events = get_events(data)

        events.sort(key=get_sort_key)
        data["events"] = events
        save_data(data)

        for ev in events:
            mode = str(ev.get("mode", ""))
            if mode == "annual":
                tag = " [Roczne]"
            elif mode == "once":
                tag = " [1-razowe (usuń)]"
            else:
                tag = " [1-razowe]"

            date_raw = str(ev.get("date", ""))
            date_formatted = format_date_to_polish(date_raw)
            text_str = str(ev.get("text", ""))
            display_text = f"{date_formatted} - {text_str}{tag}"
            self.events_list.addItem(display_text)

    def add_event(self) -> None:
        text = self.event_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Błąd", "Wpisz treść wydarzenia!")
            return

        selected_qdate = self.calendar.selectedDate()

        if self.radio_annual.isChecked():
            mode = "annual"
            date_str = selected_qdate.toString("MM-dd")
        elif self.radio_once.isChecked():
            mode = "once"
            date_str = selected_qdate.toString("yyyy-MM-dd")
        else:
            mode = "single"
            date_str = selected_qdate.toString("yyyy-MM-dd")

        new_ev: Dict[str, Any] = {
            "date": date_str,
            "text": text,
            "mode": mode
        }

        data = load_data()
        events = get_events(data)
        events.append(new_ev)
        data["events"] = events
        save_data(data)

        self.event_input.clear()
        self.refresh_list()

    def delete_event(self) -> None:
        current_row = self.events_list.currentRow()
        if current_row < 0:
            return

        data = load_data()
        events = get_events(data)
        if 0 <= current_row < len(events):
            del events[current_row]
            data["events"] = events
            save_data(data)
        self.refresh_list()


class MainWindow(QWidget):
    def __init__(self, app_ref: QApplication) -> None:
        super().__init__()
        self.app_ref = app_ref
        self.setWindowTitle("Przypominajka")
        self.setMinimumWidth(420)

        data = load_data()
        self.is_dark_mode: bool = bool(data.get("dark_mode", True))

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(6)

        today_full = datetime.now().strftime("%d.%m.%Y")
        header = QLabel(f"Dzisiaj: {today_full}")
        header.setObjectName("Header")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEME_ACCENTS.keys()))

        saved_theme = str(data.get("theme", "Fioletowy"))
        if saved_theme in THEME_ACCENTS:
            self.theme_combo.setCurrentText(saved_theme)

        self.theme_combo.currentTextChanged.connect(self.change_theme)

        self.mode_btn = QPushButton()
        self.mode_btn.setObjectName("ThemeToggleBtn")
        self.mode_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_btn.clicked.connect(self.toggle_mode)
        self.update_mode_button_icon()

        top_bar.addWidget(header, alignment=Qt.AlignmentFlag.AlignVCenter)
        top_bar.addStretch()
        top_bar.addWidget(self.theme_combo, alignment=Qt.AlignmentFlag.AlignVCenter)
        top_bar.addWidget(self.mode_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(top_bar)

        sub_header = QLabel("Wydarzenia na dziś:")
        sub_header.setObjectName("SubHeader")
        layout.addWidget(sub_header)

        self.today_list = QListWidget()
        self.today_list.setObjectName("TodayList")
        layout.addWidget(self.today_list)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)

        self.manage_btn = QPushButton("Zarządzaj")
        self.manage_btn.clicked.connect(self.open_manager)

        self.close_btn = QPushButton("Zamknij")
        self.close_btn.clicked.connect(self.close)

        btn_layout.addWidget(self.manage_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.apply_current_style()
        self.check_today_events()

    def update_mode_button_icon(self) -> None:
        self.mode_btn.setText("☀️" if self.is_dark_mode else "🌙")

    def toggle_mode(self) -> None:
        self.is_dark_mode = not self.is_dark_mode
        self.update_mode_button_icon()

        data = load_data()
        data["dark_mode"] = self.is_dark_mode
        save_data(data)

        self.apply_current_style()

    def change_theme(self, theme_name: str) -> None:
        data = load_data()
        if str(data.get("theme")) != theme_name:
            data["theme"] = theme_name
            save_data(data)

        self.apply_current_style()

    def apply_current_style(self) -> None:
        current_theme = self.theme_combo.currentText()
        qss = get_theme_qss(current_theme, self.is_dark_mode)
        self.app_ref.setStyleSheet(qss)

    def check_today_events(self) -> None:
        self.today_list.clear()
        data = load_data()
        events = get_events(data)

        today_dt = datetime.now()
        today_ymd = today_dt.strftime("%Y-%m-%d")
        today_md = today_dt.strftime("%m-%d")

        today_events: List[Dict[str, Any]] = []
        remaining_events: List[Dict[str, Any]] = []

        for ev in events:
            mode = str(ev.get("mode", ""))
            date_str = str(ev.get("date", ""))
            is_today = False

            if mode == "annual" and date_str == today_md:
                is_today = True
            elif mode in ("once", "single") and date_str == today_ymd:
                is_today = True

            if is_today:
                today_events.append(ev)
                if mode != "once":
                    remaining_events.append(ev)
            else:
                remaining_events.append(ev)

        data["events"] = remaining_events
        save_data(data)

        if today_events:
            for ev in today_events:
                text_str = str(ev.get("text", ""))
                tag = " (usunięto z bazy)" if str(ev.get("mode")) == "once" else ""
                self.today_list.addItem(f"• {text_str}{tag}")
        else:
            self.today_list.addItem("• Brak zaplanowanych wydarzeń")

    def open_manager(self) -> None:
        dialog = ManagerDialog(self)
        dialog.exec()
        self.check_today_events()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())