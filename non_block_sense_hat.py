import threading
from sense_hat import SenseHat


class NonBlockSenseHat (SenseHat):
    def repeat_message(
            self,
            text_string,
            scroll_speed=.1,
            text_colour=[255, 255, 255],
            back_colour=[0, 0, 0]
        ):
        """
        Scrolls a string of text across the LED matrix using the specified
        speed and colours
        """

        # We must rotate the pixel map left through 90 degrees when drawing
        # text, see _load_text_assets
        previous_rotation = self._rotation
        self._rotation -= 90
        if self._rotation < 0:
            self._rotation = 270
        dummy_colour = [None, None, None]
        string_padding = [dummy_colour] * 64
        letter_padding = [dummy_colour] * 8
        # Build pixels from dictionary
        scroll_pixels = []
        scroll_pixels.extend(string_padding)
        for s in text_string:
            scroll_pixels.extend(self._trim_whitespace(self._get_char_pixels(s)))
            scroll_pixels.extend(letter_padding)
        scroll_pixels.extend(string_padding)
        # Recolour pixels as necessary
        coloured_pixels = [
            text_colour if pixel == [255, 255, 255] else back_colour
            for pixel in scroll_pixels
        ]
        # Shift right by 8 pixels per frame to scroll
        scroll_length = len(coloured_pixels) // 8

        def scroll_message(interrupt):
            while True:
                for i in range(scroll_length - 8):
                    if interrupt.is_set():
                        self.set_pixels([[0, 0, 0]] * 64)
                        self._rotation = previous_rotation
                        return

                    start = i * 8
                    end = start + 64
                    self.set_pixels(coloured_pixels[start:end])
                    time.sleep(scroll_speed)

        interrupt = threading.Event()
        thread = threanding.Thread(target=scroll_message, args=[interrupt])
        thread.start()

        return (thread, interrupt)
