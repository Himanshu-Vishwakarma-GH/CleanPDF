
class Theme:
    COMMON_FONT = "font-family: 'Segoe UI', 'Inter', 'Roboto', 'Helvetica Neue', sans-serif;"
    
    # ... Light theme omitted for brevity as we are in Dark Mode ...

    DARK = {
        "window": f"background-color: #121212; color: #E0E0E0; {COMMON_FONT}", 
        
        "sidebar": f"""
            QListWidget {{
                background-color: #1A1A1A; 
                border: none;
                border-right: 1px solid #2D2D2D;
                outline: none;
                font-size: 16px; 
                padding-top: 20px;
                {COMMON_FONT}
            }}
            QListWidget::item {{
                height: 50px; /* Reduced from 60px to fit all items */
                padding-left: 25px;
                color: #A0A0A0;
                border-left: 3px solid transparent;
            }}
            QListWidget::item:selected {{
                background-color: #252525;
                color: #FFFFFF;
                font-weight: 600;
                border-left: 3px solid #4DAAF9;
            }}
            QListWidget::item:hover {{
                background-color: #222222;
            }}
        """,
        
        "pageHeader": f"font-size: 36px; font-weight: 700; color: #FFFFFF; margin-bottom: 5px; {COMMON_FONT} letter-spacing: -0.5px;", 
        "pageDesc": f"font-size: 18px; color: #999; margin-bottom: 35px; line-height: 1.5; {COMMON_FONT}", 
        
        "list_widget": f"""
             QListWidget {{
                border: 2px dashed #444; 
                border-radius: 12px;
                background-color: #1E1E1E;
                color: #EEE;
                font-size: 16px; /* Increased */
                padding: 15px;
            }}
            QListWidget::item {{
                padding: 12px;
                background-color: #2D2D2D;
                border-radius: 6px;
                margin-bottom: 8px;
            }}
        """,
        
        "actionButton": f"""
            QPushButton {{
                background-color: #0066CC;
                color: white;
                font-size: 18px; /* Increased from 16px */
                font-weight: 700;
                border-radius: 8px;
                padding: 15px 30px;
                {COMMON_FONT}
            }}
            QPushButton:hover {{ background-color: #4DAAF9; }}
            QPushButton:pressed {{ background-color: #005BB5; }}
            QPushButton:disabled {{ background-color: #333; color: #555; }}
        """,
        
        "homeCard": f"""
            QPushButton {{
                background-color: #252525;
                color: #EEE;
                border: 1px solid #333;
                border-radius: 16px;
                padding: 25px;
                font-size: 20px; /* Big Card Text */
                font-weight: 600;
                text-align: left;
                {COMMON_FONT}
            }}
            QPushButton:hover {{
                background-color: #2D2D2D;
                border: 1px solid #4DAAF9;
            }}
        """,
        
        "inputField": f"""
            background-color: #2D2D2D;
            color: white;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 14px;
            font-size: 16px;
            {COMMON_FONT}
        """,
        
        "statusBar": "QStatusBar { background-color: #007ACC; color: white; min-height: 30px; font-size: 14px; }" 
    }
