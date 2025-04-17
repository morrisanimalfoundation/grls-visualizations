import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import argparse
from typing import List
import settings

def relative_luminance(rgb):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast_ratio(rgb1, rgb2):
    lum1 = relative_luminance(rgb1)
    lum2 = relative_luminance(rgb2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

def check_plot_accessibility(fig: plt.Figure) -> List[str]:
    issues = []
    for ax in fig.get_axes():
        if not ax.get_title():
            issues.append("Missing title")
        if not ax.get_xlabel():
            issues.append("Missing X-axis label")
        if not ax.get_ylabel():
            issues.append("Missing Y-axis label")

        for text in ax.texts:
            face_color = ax.get_facecolor()
            text_color = mpl.colors.to_rgb(text.get_color())
            bg_color = face_color[:3] if len(face_color) == 4 else face_color
            ratio = contrast_ratio(text_color, bg_color)
            if ratio < 4.5:
                issues.append(f"Low contrast text at '{text.get_text()}' (ratio: {ratio:.2f})")

        if len(ax.lines) + len(ax.patches) > 1 and not ax.get_legend():
            issues.append("Missing legend for multi-series plot")

        # Final check and output
        if issues:
            print(f"\n🐞Accessibility issues found 😭")
            for issue in issues:
                print(f" - {issue}")
        else:
            print(f"✅ '{args.filename}' passed all accessibility checks.")


def check_plot_file(filename: str):
    full_file_path = settings.vizpath + '/' + filename
    if not os.path.exists(full_file_path):
        print(f"❌ File '{full_file_path}' not found.")
        return

    img = plt.imread(full_file_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis("off")
    return fig


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check matplotlib-generated plots for basic accessibility compliance."
    )
    parser.add_argument(
        "filename",
        type=str,
        help="Path to the plot image file (e.g., sex_status.png)"
    )
    args = parser.parse_args()
    figure = check_plot_file(args.filename)
    check_plot_accessibility(figure)
