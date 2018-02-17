from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Song, User

engine = create_engine('sqlite:///SongCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create first user
user = User(name="Tim McCloskey", email="tim.v.mccloskey@gmail.com",
            picture='https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg')  # noqa
session.add(user)
session.commit()

#  Categories
category = Category(user_id=1, name="Swing")
session.add(category)
session.commit()

category = Category(user_id=1, name="Blues")
session.add(category)
session.commit()

category = Category(user_id=1, name="Jump Blues")
session.add(category)
session.commit()

category = Category(user_id=1, name="Rockabilly")
session.add(category)
session.commit()

category = Category(user_id=1, name="Boogie Woogie")
session.add(category)
session.commit()


# Add Songs
song = Song(user_id=1, title="One O'Clock Jump", artist="Benny Goodman",
            link="https://www.youtube.com/watch?v=utfwhkDmM1g", category_id=1)
session.add(song)
session.commit()

song = Song(user_id=1, title="Let Me Off Uptown", artist="Gene Krupa",
            link="https://www.youtube.com/watch?v=GHCaxVCXNIc", category_id=1)
session.add(song)
session.commit()

song = Song(user_id=1, title="Swinging The Blues", artist="Count Basie",
            link="https://www.youtube.com/watch?v=Rxg_kA6YaYk", category_id=1)
session.add(song)
session.commit()

song = Song(user_id=1, title="Things Aint What They Used To Be",
            artist="Count Basie",
            link="https://www.youtube.com/watch?v=yzPgYo19AsQ", category_id=1)
session.add(song)
session.commit()

song = Song(user_id=1, title="C Jam Blues",
            artist="Wynton Marsalas and the Lincoln Center Jazz Orchestra ",
            link="https://www.youtube.com/watch?v=mSBmMswu17k", category_id=1)
session.add(song)
session.commit()

song = Song(user_id=1, title="Bassology", artist="Willie Dixon",
            link="https://www.youtube.com/watch?v=UcqqyL-Y6Go", category_id=2)
session.add(song)
session.commit()

song = Song(user_id=1, title="The Same Thing", artist="Willie Dixon",
            link="https://www.youtube.com/watch?v=QoU-CKvhjgU", category_id=2)
session.add(song)
session.commit()

song = Song(user_id=1, title="Juke", artist="Little Walter",
            link="https://www.youtube.com/watch?v=uiGpv-UeiDI", category_id=2)
session.add(song)
session.commit()

song = Song(user_id=1, title="Sweet Home Chicago", artist="Buddy Guy",
            link="https://www.youtube.com/watch?v=ZEmvBdRLg4k", category_id=2)
session.add(song)
session.commit()

song = Song(user_id=1, title="Saint Louis Blues", artist="Silvan Zingg",
            link="https://www.youtube.com/watch?v=WcQx63n6s2M", category_id=2)
session.add(song)
session.commit()

song = Song(user_id=1, title="Statesboro Blues", artist="Taj Mahal",
            link="https://www.youtube.com/watch?v=SBMzfKaExd0", category_id=2)
session.add(song)
session.commit()

song = Song(user_id=1, title="Shufflin & Rollin", artist="Buddy Johnson",
            link="https://www.youtube.com/watch?v=O7lL_FV9vTU", category_id=3)
session.add(song)
session.commit()

song = Song(user_id=1, title="Alright, okay, you win", artist="Ella Johnson ",
            link="https://www.youtube.com/watch?v=_lwdD-AlkUQ", category_id=3)
session.add(song)
session.commit()

song = Song(user_id=1, title="Just a Gigolo & I Ain't Go Nobody",
            artist="Louis Prima ",
            link="https://www.youtube.com/watch?v=O-a8kLtJSJ4", category_id=3)
session.add(song)
session.commit()

song = Song(user_id=1, title="Choo Choo Ch'Boogie", artist="Louis Jordan",
            link="https://www.youtube.com/watch?v=NwAnNzfZ7H0", category_id=3)
session.add(song)
session.commit()

song = Song(user_id=1, title="My New Papa's Got to Have Everything",
            artist="Nellie Lutcher",
            link="https://www.youtube.com/watch?v=_xk7Jd6A8O4", category_id=3)
session.add(song)
session.commit()

song = Song(user_id=1, title="Guitar Boogie", artist="Arthur Smith",
            link="https://www.youtube.com/watch?v=2sT0Za4Rge0", category_id=4)
session.add(song)
session.commit()

song = Song(user_id=1, title="Whole Lotta Shakin Going On",
            artist="Wanda Jackson",
            link="https://www.youtube.com/watch?v=rQX5yGZvjzs", category_id=4)
session.add(song)
session.commit()

song = Song(user_id=1, title="Lotta Lovin", artist="Gene Vincent",
            link="https://www.youtube.com/watch?v=K3bIqQrWiSk", category_id=4)
session.add(song)
session.commit()

song = Song(user_id=1, title="All Shook Up", artist="Elvis Presley",
            link="https://www.youtube.com/watch?v=3rQEbQJx5Bo", category_id=4)
session.add(song)
session.commit()

song = Song(user_id=1, title="It's Late", artist="Ricky Nelson",
            link="https://www.youtube.com/watch?v=nBnhQ_wjkP8", category_id=4)
session.add(song)
session.commit()

song = Song(user_id=1, title="medley",
            artist="MICKE MUSTER AND LINDA GAIL LEWIS",
            link="https://www.youtube.com/watch?v=xnLsVWX_E9c", category_id=4)
session.add(song)
session.commit()

song = Song(user_id=1, title="Sentimental Journey", artist="Silvan Zingg",
            link="https://www.youtube.com/watch?v=LTqYd9rMiDk", category_id=5)
session.add(song)
session.commit()

song = Song(user_id=1, title="Heat It Up!", artist="Axel Zwingenberger",
            link="https://www.youtube.com/watch?v=u4P4nXkz0Ks", category_id=5)
session.add(song)
session.commit()

song = Song(user_id=1, title="boogie +++", artist="Martin Pyrker",
            link="https://www.youtube.com/watch?v=1FGEnCNcIN8", category_id=5)
session.add(song)
session.commit()

song = Song(user_id=1, title="Death Ray Boogie", artist="Joja Wendt",
            link="https://www.youtube.com/watch?v=S2OnzfciEt8", category_id=5)
session.add(song)
session.commit()

song = Song(user_id=1, title="Come On In if You're Coming",
            artist="Dana Gillespie & Joachim Palden",
            link="https://www.youtube.com/watch?v=rRFija0otKc", category_id=5)
session.add(song)
session.commit()
