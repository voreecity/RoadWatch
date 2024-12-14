from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QFileDialog, QCheckBox, QPushButton, QVBoxLayout, \
    QHBoxLayout
from PyQt6.QtGui import QFont


class MainWindow(QWidget):
    speed_checkbox_value = False
    classname_checkbox_value = False
    oncoming_checkbox_value = False
    outgoing_checkbox_value = False

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Traffic Cam Analysis')
        font = QFont("Helvetica", 12, QFont.Weight.Medium)
        self.setFont(font)

        # Create the layout
        layout = QVBoxLayout()

        # Add the video file input
        self.video_file_label = QLabel('Please enter the location of the video file')
        layout.addWidget(self.video_file_label)

        self.video_file_input = QLineEdit()
        self.video_file_button = QPushButton('Browse')
        self.video_file_button.clicked.connect(self.browse_video_file)
        video_file_layout = QHBoxLayout()
        video_file_layout.addWidget(self.video_file_input)
        video_file_layout.addWidget(self.video_file_button)
        layout.addLayout(video_file_layout)

        # Add the checkboxes
        self.speed_checkbox = QCheckBox('Speed')
        self.classname_checkbox = QCheckBox('Vehicle Class')
        self.outgoing_checkbox = QCheckBox('Outgoing')
        self.oncoming_checkbox = QCheckBox('Oncoming')
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.speed_checkbox)
        checkbox_layout.addWidget(self.classname_checkbox)
        checkbox_layout.addWidget(self.outgoing_checkbox)
        checkbox_layout.addWidget(self.oncoming_checkbox)
        layout.addLayout(checkbox_layout)

        # Add the buttons
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.ok_button_clicked)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Set the layout
        self.setLayout(layout)

    def browse_video_file(self):
        file_dialog = QFileDialog()
        video_file_location = file_dialog.getOpenFileName(self, 'Select Video File')[0]
        if video_file_location:
            self.video_file_input.setText(video_file_location)

    def ok_button_clicked(self):
        video_file_location = self.video_file_input.text()
        if video_file_location:
            speed_checkbox_value = self.speed_checkbox.isChecked()
            classname_checkbox_value = self.classname_checkbox.isChecked()
            outgoing_checkbox_value = self.outgoing_checkbox.isChecked()
            oncoming_checkbox_value = self.oncoming_checkbox.isChecked()
            self.process_video(video_file_location, speed_checkbox_value, classname_checkbox_value,
                               outgoing_checkbox_value, oncoming_checkbox_value)
        else:
            print('No video file selected.')

    def cancel_button_clicked(self):
        print('The user cancelled the operation.')
        self.close()

    def process_video(self, video_file_location, speed_checkbox_value, classname_checkbox_value,
                      outgoing_checkbox_value, oncoming_checkbox_value):
        from video_processing import process_video
        process_video(video_file_location, speed_checkbox_value, classname_checkbox_value, outgoing_checkbox_value,
                      oncoming_checkbox_value)
