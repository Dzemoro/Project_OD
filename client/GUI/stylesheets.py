#dialogStyle = "background-color: rgb(57, 162, 219)\n"""
dialogStyle = ("background-color: #334257\n")

encryptDropDownStyle = ("QComboBox{\n"
"    font: 14pt \"Univers\";\n"
"    padding-left: 10px;\n"
"    background-color: #476072;\n"
"    border: 3px solid #548CA8;\n"
"    color: #EEEEEE;\n"
"    radius: 8px;\n"
"    border-radius: 8px;\n"
"    selection-background-color: #548CA8;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    color: white;\n"
"    background-color: #476072;\n"
"    border: 0px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"   image: url(:/images/dropdown.png);\n"
"   width: 14px;\n"
"   height: 14px;\n"
"   padding-right: 10px;\n"
"   border: 0;\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"     image: url(:/images/dropdown_on.png);\n"
"}\n"
"QListView{\n"
"  margin-top: 10px;\n"
"  color: #EEEEEE;\n"
"  border: 3px solid #548CA8;\n"
"  radius: 8px;\n"
"  border-radius: 8px;\n"
"  selection-color: white;\n"
"  selection-background-color: #548CA8;\n"
"  outline: none;\n"
"  cursor: pointer;\n"
"  \n"
"}\n""")

messagesAreaStyle = ("QTextBrowser\n"
"{\n"
"    font: 12pt \"Univers\";\n"
"    background-color: #476072;\n"
"    radius: 12px;\n"
"    border-radius: 8px;\n"
"    border: 3px solid #548CA8;\n"
"    padding-left: 10px;\n"
"    color: #EEEEEE;\n"
"}\n""")

scrollBarStyle = ("QScrollBar:vertical {\n"
"        border-left: 3px solid #548CA8;\n"
"        background: #548CA8;\n"
"    }\n"
"    QScrollBar::handle:vertical {\n"
"        background: #39A2DB;\n"
"        border-radius: 20px;\n"
"    }\n"
"    QScrollBar::add-line:vertical {\n"
"        background: none;\n"
"        height: 2px;\n"
"        subcontrol-position: bottom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"    QScrollBar::sub-line:vertical {\n"
"        background: none;\n"
"        height: 2px;\n"
"        subcontrol-position: top left;\n"
"        subcontrol-origin: margin;\n"
"        position: absolute;\n"
"    }\n"
"    QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"        background: none;\n"
"    }\n"
"    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"        background: none;\n"
"    }\n""")

messageInputStyle = ("QTextEdit{\n"
"    color: #EEEEEE;\n"
"    padding-left: 10px;\n"
"    font: 12pt \"Univers\";\n"
"    border: 3px solid;\n"
"    border-color: #548CA8;\n"
"    border-radius: 8px;\n"
"    background: #476072;\n"
"}\n""")

sendButtonStyle = ("QPushButton\n"
"{\n"
"    font: 8pt \"Univers\";\n"
"    color: #EEEEEE;\n"
"    font-size: 14px;\n"
"    background-color: #476072;\n"
"    radius: 8px;\n"
"    border-radius: 8px;\n"
"    border: 3px solid #548CA8;\n"
"    letter-spacing: 2px;\n"
"    outline: none; \n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #548CA8;\n"
"    border: 3px solid #EEEEEE;\n"
"    color: #EEEEEE;\n"
"}\n""")

buttonStyle = ("QPushButton\n"
"{\n"
"    font: 8pt \"Univers\";\n"
"    color: #EEEEEE;\n"
"    font-size: 14px;\n"
"    background-color: #476072;\n"
"    radius: 8px;\n"
"    border-radius: 8px;\n"
"    border: 3px solid #548CA8;\n"
"    letter-spacing: 2px;\n"
"    outline: none; \n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #548CA8;\n"
"    border: 3px solid #EEEEEE;\n"
"    color: #EEEEEE;\n"
"}\n""")

labelStyle = ("QLabel{\n"
"    font: 12pt \"Univers\";\n"
"    color: #EEEEEE;\n"
"    font-size: 14px;\n"
"    text-align: left;\n"
"    margin-left: -200px;    \n"
"}\n"
"")

inputStyle = ("QLineEdit{\n"
"    color: #EEEEEE;\n"
"    padding-left: 10px;\n"
"    font: 12pt \"Univers\";\n"
"    border: 3px solid;\n"
"    border-color: #548CA8;\n"
"    border-radius: 8px;\n"
"    background: #476072;\n"
"}\n"
"\n"
"")

startBtnStartStyle = ("QPushButton\n"
"{\n"
"    font: 8pt \"Univers\";\n"
"    color: #EEEEEE;\n"
"    font-size: 14px;\n"
"    background-color: #007f5f;\n"
"    radius: 8px;\n"
"    border-radius: 8px;\n"
"    border: 5px solid #2b9348;\n"
"    letter-spacing: 2px;\n"
"    outline: none; \n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #2b9348;\n"
"    border: 5px solid #007f5f;\n"
"}\n""")

startBtnStopStyle = ("QPushButton\n"
"{\n"
"    font: 8pt \"Univers\";\n"
"    color: #EEEEEE;\n"
"    font-size: 13px;\n"
"    radius: 8px;\n"
"    border-radius: 8px;\n"
"    letter-spacing: 1px;\n"
"    background-color: #a01a58;\n"
"    border: 5px solid #b7094c;\n"
"    outline: none; \n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #b7094c;\n"
"    border: 5px solid #a01a58;\n"
"}\n""")

usersAreaStyle = ("QListWidget\n"
"{\n"
"    font: 12pt \"Univers\";\n"
"    background-color: #476072;\n"
"    radius: 12px;\n"
"    border-radius: 8px;\n"
"    border: 3px solid #548CA8;\n"
"    padding-left: 10px;\n"
"    color: #EEEEEE;\n"
"}\n""")

phonebookLabelStyle = ("QLabel{\n"
"    font: 14pt \"Univers\";\n"
"    color: #EEEEEE;\n"
"    text-align: left;\n"
"    margin-left: -200px;    \n"
"}\n"
"")