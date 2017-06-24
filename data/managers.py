from iwbt import get_session
from iwbt.models.rivers import Area, Gauge, GaugeData, River, Rapid, Section
import random


class Busboy(object):
    """ The busboy clears tables """
    def __init__(self, app):
        self.app = app
        self.MODELS = [GaugeData, Rapid, Gauge, Section, River, Area]

    def run(self):
        for model in self.MODELS:
            self._clear_table(model)

    def _clear_table(self, model):
        session = get_session(self.app)
        session.query(model).delete()
        session.commit()
        session.close()



class DataSpoofer(object):
    def __init__(self, app):
        self.app = app

    def run(self):
        self._populate_areas()
        self._populate_rivers()
        self._populate_sections()
        self._populate_rapids()
        self._populate_gauges()


    def _populate_areas(self):
        session = get_session(self.app)
        for name in ['Blue Ridge', 'Cumberland', 'Balsams', 'Pisgah']:
            session.add(Area(name=name))
        session.commit()
        session.close()

    def _populate_gauges(self):
        pass

    def _populate_rivers(self):
        session = get_session(self.app)
        areas = session.query(Area).all()
        for area in areas:
            self._create_random_river(area, session)
            self._create_random_river(area, session)

    def _populate_sections(self):
        session = get_session(self.app)
        rivers = session.query(River).all()
        for river in rivers:
            for section in ['Section 1', 'Section 2', 'Lower']:
                session.add(Section(name=section, area_id=river.area_id, river_id=river.id))
        session.commit()
        session.close()

    def _populate_rapids(self):
        session = get_session(self.app)
        sections = session.query(Section).all()
        for section in sections:
            for i in range(6):
                self._create_random_rapid(section, session)

    def _create_random_rapid(self, section, session=None):
        if not session:
            session = get_session(self.app)
        session.add(Rapid(name=self._get_random_rapid_name(),
                          river_id=section.river_id,
                          section_id=section.id,
                          rating=random.randrange(2, 5)))
        session.commit()

    def _create_random_river(self, area, session=None):
        if not session:
            session = get_session(self.app)
        session.add(River(name=self._get_random_river_name(), area_id=area.id))
        session.commit()

    def _get_random_river_name(self):
        random_river_names = [
            'Chattooga', 'Tennessee', 'Toccoa', 'Tomatola', 'Toogelah',
            'Citico', 'Shit', 'Toxaway', 'Tomassee', 'Seneca',
            'Sequatchee', 'Savannah', 'Qualatchee', 'Owassa',
            'Nucassee', 'Nantahala', 'Kunnesee', 'Keowee', 'Kanuga',
            'Jutaculla', 'Hemptown', 'Euharlee', 'Frogtown', 'Cheeowhee',
            'Ayuhwasee', 'Choquata', 'Conasauga', 'Cullasagee', 'Cullowhee',
            'Fightingtown', 'Farttown'
        ]
        river = random.choice(random_river_names)
        return "{} {}".format(river, random.choice(['River', 'Creek']))

    def _get_random_rapid_name(self):
        random_rapid_names = [
            'Terminator', 'Godzilla', 'Ghostrider', 'Oblivion', 'Gnashing Jaws of Death',
            'Screaming Left', 'Jawbone', 'Entrance', 'Coming Home Sweet Jesus', 'Toaster',
            'Fuzzy Little Box of Kittens', 'Boof or Die', 'Wet Ass Rapid', 'Shipwreck',
            'Pillow', 'Insignificant', 'Holy Shit', 'Almost Always', 'Grim Reaper',
            'Jaws', 'Yardsale', 'Hammer Factor', 'Gorilla', 'Hydro', 'Sunshine', 'Go Left and Die',
            'Heavy Water', 'Oceana', 'Bridal Veil', 'Gauntlet', 'Submarine', 'Marginal Monster',
            'Pinball', 'Widow Maker', 'Damnation Alley', 'Vortex', 'Surfers', 'Rock Jumble',
            'Woodall', '7 Foot Falls', 'Long Creek', 'Corkscrew', 'Boxcar', 'Gravity', 'Blind Falls',
            'Swiss Cheese', 'Shit Kicker', 'Knuckles', 'Blowjob', 'Dry Falls', 'The Notch',
            'Razorback', 'Island Rapid', 'Vortex', 'The Clog', 'Power Slide', 'Groove Tube',
            'Toiled Bowl', 'Stairstep', 'Corner Pocket', 'Side Pocket', 'Highway to Heaven',
            'Drunk Tank', 'Arch Nemesis', 'Double Undercut', 'Jailhouse', 'Cyclops',
            'Cave Falls', 'Jedi Training', 'Headless Horwseman', 'Mortal Kombat', 'Mangler'
        ]
        return random.choice(random_rapid_names)