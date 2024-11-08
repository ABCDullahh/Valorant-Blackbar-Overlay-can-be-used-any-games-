# Game Blackbar Overlay & Optimizer (Valorant)

Game Overlay & Optimizer is a Python application tailored for gamers to enhance performance and create a customizable gameplay experience. The overlay feature provides adjustable black bars on the left and right sides of the screen, simulating a 4:3 aspect ratio on a widescreen display. This aspect ratio adjustment can create a more immersive experience, although it may partially obscure game elements (such as the map) on the sides of the screen.

![image](https://github.com/user-attachments/assets/959f5011-a0d1-4dd1-9920-71497ffa74fe)

---

## Features

- **Adjustable Overlay with Left and Right Black Bars**: Customize the overlay to include black bars on the left and right sides, creating a narrower aspect ratio like 4:3. Note that this adjustment may hide parts of the in-game map or other side elements.
- **Game Performance Optimization**:
  - Set the game process to high priority.
  - Recommend closing CPU- and memory-intensive background applications.
  - Enable maximum performance mode for NVIDIA GPUs.
- **Customizable Shortcut Key**: Define a shortcut key for quickly toggling the overlay on and off.
- **Modern Tkinter GUI**: A clean, user-friendly interface for easy access to all controls and settings.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or later. Install the following required libraries:

- `tkinter` (included with Python)
- `pygame` (for overlay rendering)
- `psutil` (for system and process management)
- `keyboard` (for global keyboard shortcuts)
- `pywin32` (for Windows-specific API functions)

To install dependencies, run:

```bash
pip install pygame psutil keyboard pywin32
```

### Installation

1. Download from latest Version

### Usage

1. **Run the Application**: Launch the script to open the main window.
2. **Set Black Bar Width**: Adjust the width of the left and right black bars using the slider in the "Black Bar Settings" section to simulate different aspect ratios.
3. **Activate/Deactivate Overlay**: Click "Activate Overlay" to enable the black bars. This will create a 4:3-like experience but may hide the game map or side elements as a side effect.
4. **Change Shortcut Key**: Customize the shortcut key to toggle the overlay easily during gameplay.
5. **Optimize Game Performance**: Use the "Optimize Performance" button to enhance game performance by adjusting system priority and closing non-essential background applications.
6. **Exit**: Use the "Exit" button to close the application.

### Overlay Tips

- **Aspect Ratio Simulation**: Setting the black bars to approximately 12.5% width on each side mimics a 4:3 aspect ratio on most screens. 
- **Side Effect**: The black bars may hide certain in-game elements, such as the map, which can affect gameplay visibility.

## Advanced Settings

- **Windows Compatibility**: This application is designed for Windows OS, as it relies on specific Win32 API functions.
- **Run as Administrator**: For full functionality (e.g., setting process priority), run the application with administrator privileges.

## Troubleshooting

- **Overlay Issues**: If the overlay is not appearing, ensure `pygame` and `pywin32` are installed correctly. Check that no other fullscreen application is active.
- **Performance Settings**: Running the application as an administrator can resolve access issues with priority settings.

## Contributing

Contributions are welcome! To contribute, fork the repository, create a new branch, and submit a pull request. Contributions that improve functionality, compatibility, or add customization options are appreciated.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Credits

Developed by **ABCDullahh**. Visit [GitHub](https://github.com/ABCDullahh) for more projects.
