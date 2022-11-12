class Validators:

    def dateValidator(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 < value <= 100000000
