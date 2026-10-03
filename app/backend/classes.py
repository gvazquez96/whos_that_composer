class Composer:

    def __init__(self, name):

        self._name = name
        self._pieces = set()

    @property
    def name(self):
        """
        Name getter
        """
        return self._name

    @property
    def pieces(self):
        """
        Pieces getter
        """
        return self._pieces

    def __repr__(self):
        return f"Composer({self._name}, {self._pieces})"

    def __str__(self):
        return f"{self._name}"

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False

    def add_piece(self, piece):
        self._pieces.add(piece)


class Piece:
    """
    Piece class containing all metadata: composer (class), piece name, year of composition, 
    catalogue number, midi file
    """

    def __init__(self, Composer, name,  year, catalogue_number, midi):
        self._composer = Composer
        self._name = name
        self._year = year
        self._catalogue = catalogue_number
        self._midi = midi

    @property
    def composer(self):
        """
        Composer getter
        """
        return self._composer

    @property
    def name(self):
        """
        Piece name getter
        """
        return self._name

    @property
    def year(self):
        """
        Year getter
        """
        return self._year

    @property
    def catalogue(self):
        """
        Catalogue getter
        """
        return self._catalogue

    @property
    def midi(self):
        """
        Midi getter
        """
        return self._midi

    def __str__(self):
        return f"Piece name: {self._name}, composer: {self._composer.name}, year: {self._year}, catalogue number: {self._catalogue}, midi: {self._midi}"

    def __repr__(self):
        return f"{self._name} {self._catalogue}"
