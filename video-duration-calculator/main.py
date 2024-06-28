import os
import platform

from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, MofNCompleteColumn
from moviepy.editor import VideoFileClip
from InquirerPy import inquirer
from tkinter import Tk, filedialog


def format_duration(duration):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def format_size(size_bytes):
    size_units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = size_bytes
    unit = size_units.pop(0)
    while size >= 1024 and size_units:
        size /= 1024
        unit = size_units.pop(0)
    return f"{size:.2f} {unit}"


def open_file_explorer():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    selected_dirs = []

    while True:
        selected_dir = filedialog.askdirectory()

        if selected_dir:
            selected_dirs.append(selected_dir)
        else:
            break
    root.destroy()
    return selected_dirs


class VideoDurationCalculator:
    def __init__(self, directories):
        self.directories = directories
        self.directory_durations = {}
        self.overall_total_duration = 0
        self.overall_total_size = 0
        self.console = Console()

    def list_files(self, dir_name):
        all_files = []
        extensions_list = ['.mp4', '.webm', '.mkv', '.flv', '.vob', '.ogv', '.ogg', '.avi', '.mov', '.wmv', '.m4v', '.3gp', '.f4v', '.asf', '.rm', '.rmvb', '.divx', '.qt', '.mts',
                           '.m2ts', '.mpeg', '.mpg', '.mxf', '.svi', '.dat']

        for entry in os.scandir(dir_name):
            if entry.is_dir():
                all_files += self.list_files(entry.path)
            elif entry.is_file() and os.path.splitext(entry.name)[1] in extensions_list:
                all_files.append(entry.path)
        return all_files

    def process_directory(self, directory):
        total_duration = 0
        total_size = 0
        results = []

        files = self.list_files(directory)

        with Progress(
                SpinnerColumn(),
                BarColumn(complete_style="red"),
                TextColumn("[progress.description]{task.description}"),
                TimeRemainingColumn(),
                MofNCompleteColumn(),
                transient=True
        ) as progress:
            self.console.print(f"[bold cyan]Processing Directory:[/bold cyan] [blue]{directory}[/blue]")

            task = progress.add_task("[green]Processing files...", total=len(files))

            for file_idx, file_path in enumerate(files, start=1):
                with VideoFileClip(file_path) as clip:
                    file_name = os.path.basename(file_path)
                    file_extension = os.path.splitext(file_path)[1]
                    file_duration = clip.duration
                    file_size = os.path.getsize(file_path)

                    total_duration += file_duration
                    total_size += file_size

                    results.append((file_name, file_extension, file_duration, file_size))

                progress.update(task, advance=1, description=f"File: {file_name}", completed=file_idx)

            self.console.clear()

        return results, total_duration, total_size

    def run(self):
        try:
            for directory in self.directories:
                results, total_duration, total_size = self.process_directory(directory)
                self.directory_durations[directory] = (results, total_duration, total_size)
                self.overall_total_duration += total_duration
                self.overall_total_size += total_size

            self.display_summary()
            self.display_details()

        except Exception as e:
            print(f"An error occurred: {e}")

    def display_summary(self):
        summary_table = Table(title="Summary Of All Directories", title_style="bold underline white reverse")
        summary_table.add_column("No", justify="left", style="cyan", no_wrap=True)
        summary_table.add_column("Directory", justify="left", style="green", no_wrap=True)
        summary_table.add_column("Total Duration", justify="left", style="blue")
        summary_table.add_column("Total Size", justify="left", style="yellow")

        for idx, (directory, (_, total_duration, total_size)) in enumerate(self.directory_durations.items(), 1):
            duration_str = format_duration(total_duration)
            size_str = format_size(total_size)
            summary_table.add_row(str(idx), directory, duration_str, size_str)

        overall_total_size_str = format_size(self.overall_total_size)
        overall_total_duration_str = format_duration(self.overall_total_duration)
        summary_table.add_section()
        summary_table.add_row("Total", "", overall_total_duration_str, overall_total_size_str, style="bold red")

        self.console.print(summary_table)

    def display_details(self):
        for idx, (directory, (results, total_duration, total_size)) in enumerate(self.directory_durations.items(), 1):
            details_table = Table(title=f"Directory: {directory}", title_style="bold underline white reverse")
            details_table.add_column("No", justify="left", style="cyan", no_wrap=True)
            details_table.add_column("Name", justify="left", style="green", no_wrap=True)
            details_table.add_column("Extension", justify="left", style="blue")
            details_table.add_column("Duration", justify="left", style="yellow")
            details_table.add_column("Size", justify="left", style="magenta")

            for file_idx, (name, extension, duration, size) in enumerate(results, 1):
                duration_str = format_duration(duration)
                size_str = format_size(size)
                details_table.add_row(str(file_idx), name, extension, duration_str, size_str)

            total_duration_str = format_duration(total_duration)
            total_size_str = format_size(total_size)
            details_table.add_section()
            details_table.add_row("Total", "", "", total_duration_str, total_size_str, style="bold red")

            self.console.print(details_table)


if __name__ == '__main__':
    console = Console()
    system = platform.system()

    if system == "Windows":
        example_path = "C:\\Users\\Username\\Videos"
    elif system == "Linux":
        example_path = "/home/username/videos"
    elif system == "Darwin":  # macOS
        example_path = "/Users/username/Videos"
    else:
        example_path = "/your/video/directory"

    choice = inquirer.select(message="Do you want to manually enter the directory path or open file explorer?", choices=["Manual Entry", "Open File Explorer"], ).execute()

    directories = []

    if choice == "Manual Entry":
        while True:
            directory = Prompt.ask(f"[bold yellow]Please enter the directory path where your videos are located (e.g., [cyan]{example_path}[/cyan])")

            if os.path.exists(directory):
                directories.append(directory)
                another = Prompt.ask("[bold yellow]Do you want to add another directory?", choices=["y", "n"], default="n")

                if another == "n":
                    break
            else:
                console.print("[bold red]The specified directory does not exist. Please check the path and try again.\n")
    elif choice == "Open File Explorer":
        directories = open_file_explorer()

        if not directories:
            console.print("[bold red]No directories were selected. Please try again.\n")
            exit(1)

    calculator = VideoDurationCalculator(directories)
    calculator.run()
