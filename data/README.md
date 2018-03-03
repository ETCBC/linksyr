# Data files from several sources in several formats


## Data originating from ETCBC

For a list of an-files, see: ~const/cur/peeters/an-list

        hannes@jakob:~$ head -n 3 ~const/cur/peeters/an-list
        # *.an to use as source for the anzb
        # $1 == "C" { include in CALAP collection }
        # $1 == "T" { include in Turgama collection }

        hannes@jakob:~$ grep '^[TC]' ~const/cur/peeters/an-list
        T       /home/mignon/eprx/eprx.an
        T       /home/eep/synheb/Turgama/P_OrManA.an
        T       /home/eep/synheb/Turgama/P_OrManB.an
        C       /projects/calap/SCCS/s.BenSira.an
        C       /projects/calap/SCCS/s.9a1.an
        C       /projects/calap/SCCS/s.Reges.an
        C       /projects/calap/P_Psalmi/P_Psalmi.an
        T       /projects/turgama/SCCS/s.Laws.an
        T       /projects/turgama/ri45/S/P_Judices.an
        T       /projects/turgama/ApBar/P_EpBarB.an
        T       /projects/turgama/ApBar/P_EpBarA.an


### CALAP project

* **Ben Sira # (13,304 woorden) (Wido)**

  **Error** This directory contains a subdirectory `data` with an `at2ps.conf` file,
  but the lexicon specified there does not provide all necessary lexemes.

  | an-file        | `/projects/calap/BenSira.an`          |
  |----------------|---------------------------------------|
  | conf-file      | `/projects/calap/data/at2ps.conf`     |
  | - alphabet     | `/projects/lib/syriac/alphabet`       |
  | - psdef        | `/projects/lib/syriac/psdef`          |
  | - lexicon      | `/projects/calap/syriac/lexicon`      |
  | - word_grammar | `/projects/calap/syriac/word_grammar` |

* **Kings (24,908 woorden) (Percy)**

  **Error** This directory contains a subdirectory `data` with an `at2ps.conf` file,
  but the lexicon specified there does not provide all necessary lexemes.
  Also the word_grammar is not correct (that should be `/home/janet/word_grammar`?).
  The same an-file is present in another location: `/projects/calap/9a1.an` ?

  | an-file        | `/projects/calap/Reges.an`            |
  |----------------|---------------------------------------|
  | conf-file      | `/projects/calap/data/at2ps.conf`     |
  | - alphabet     | `/projects/lib/syriac/alphabet`       |
  | - psdef        | `/projects/lib/syriac/psdef`          |
  | - lexicon      | `/projects/calap/syriac/lexicon`      |
  | - word_grammar | `/projects/calap/syriac/word_grammar` |

* **Psalms (Psalms 1-25? or 30?)**

  **Error** It is not clear up to where the Psalms have been annotated - either up to Psalm 25
  or Psalm 30. It is also not clear which `word_grammar` and `lexicon` should be used,
  as the `lexicon` in the same directory (also specified in `at2ps.conf` in the same
  directory) does not provide all the necessary lexemes.

  | an-file        | `/projects/calap/P_Psalmi/P_Psalmi.an` |
  |----------------|----------------------------------------|
  | conf-file      | `/projects/calap/P_Psalmi/at2ps.conf`  |
  | - alphabet     | `/projects/lib/syriac/alphabet`        |
  | - psdef        | `/projects/calap/P_Psalmi/syrpsd`      |
  | - lexicon      | `/projects/calap/P_Psalmi/syrlex`      |
  | - word_grammar | `/projects/calap/P_Psalmi/syrwgr`      |


### Turgama project

* **Judges**

  The same an-file is present in another location:
  `/projects/turgama/ri45/S/P_Judices.an`

  | an-file        | `/home/wido/Judges/Judges_Syr/P_Judices.an` |
  |----------------|---------------------------------------------|
  | conf-file      | `/home/wido/Judges/Judges_Syr/at2ps.conf`   |
  | - alphabet     | `/projects/lib/syriac/alphabet`             |
  | - psdef        | `/home/wido/Judges/Judges_Syr/syrpsd`       |
  | - lexicon      | `/home/wido/Judges/Judges_Syr/syrlex`       |
  | - word_grammar | `/home/wido/Judges/Judges_Syr/syrwgr`       |

* **Epistle of Baruch**

  | **an-file**    | **`/projects/turgama/ApBar/P_EpBarB.an`** |
  |----------------|-------------------------------------------|
  | **an-file**    | **`/projects/turgama/ApBar/P_EpBarB.an`** |
  | conf-file      | `/projects/turgama/ApBar/at2ps.conf`      |
  | - alphabet     | `/projects/lib/syriac/alphabet`           |
  | - psdef        | `/projects/turgama/ApBar/syrpsd`          |
  | - lexicon      | `/projects/turgama/ApBar/syrlex`          |
  | - word_grammar | `/projects/turgama/ApBar/syrwgr`          |

* **Prayer of Manasseh**

  The files referenced in `at2ps.conf` in the directory of the an-files do not exist.
  It seems to work to use the `at2ps.conf` in the Judges_Syr directory.

  | **an-file**    | **`/home/eep/synheb/Turgama/P_OrManA.an`** |
  |----------------|--------------------------------------------|
  | **an-file**    | **`/home/eep/synheb/Turgama/P_OrManB.an`** |
  | ~~conf-file~~  | ~~`/home/eep/synheb/Turgama/at2ps.conf`~~  |
  | conf-file      | `/home/wido/Judges/Judges_Syr/at2ps.conf`  |
  | - alphabet     | `/projects/lib/syriac/alphabet`            |
  | - psdef        | `/home/wido/Judges/Judges_Syr/syrpsd`      |
  | - lexicon      | `/home/wido/Judges/Judges_Syr/syrlex`      |
  | - word_grammar | `/home/wido/Judges/Judges_Syr/syrwgr`      |

* **Book of the Laws of the Countries (Dirk Bakker) (5,277 woorden)**

  | an-file        | `/home/dirk/nomoos/Laws.an`     |
  |----------------|---------------------------------|
  | conf-file      | `/home/dirk/nomoos/at2ps.conf`  |
  | - alphabet     | `/projects/lib/syriac/alphabet` |
  | - psdef        | `/home/dirk/nomoos/syrpsd`      |
  | - lexicon      | `/home/dirk/nomoos/syrlex`      |
  | - word_grammar | `/home/dirk/nomoos/syrwgr`      |


### Efrem projects (Polemics Visualized, LinkSyr)

* **Efrem - Prose Refutations X (Mignon)**

  | an-file        | `/home/mignon/eprx/eprx.an`      |
  |----------------|----------------------------------|
  | conf-file      | `/home/mignon/eprx/at2ps.conf`   |
  | - alphabet     | `/projects/lib/syriac/alphabet`  |
  | - lexicon      | `/home/mignon/eprx/lexicon`      |
  | - psdef        | `/home/mignon/eprx/psdef`        |
  | - word_grammar | `/home/mignon/eprx/word_grammar` |

* **Efrem - Sermon on Jonah and Nineveh (Geert Jan - work in progress)**

  | an-file        | `/home/geertjan/efrem/preek.an`   |
  |----------------|-----------------------------------|
  | conf-file      | `/home/geertjan/efrem/at2ps.conf` |
  | - alphabet     | `/projects/lib/syriac/alphabet`   |
  | - lexicon      | `/home/geertjan/efrem/lexicon`    |
  | - psdef        | `/projects/turgama/psdef`         |
  | - word_grammar | `/projects/turgama/word_grammar`  |


## Data from other sources

* BFBS New Testament (British Foreign Bible Society) (109,640 woorden)

  as part of SEDRA-III database (George Kiraz), and as part of Syromorph software:

  - `syromorph/data/syriac/syromorph/all-ordered.txt`

* Peeters
  - ~const/cur/peeters/incoming
