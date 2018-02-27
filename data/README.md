Data files from several sources in several formats.

Data originating from ETCBC:

* CALAP project

  - Ben Sira
    /projects/calap/BenSira.an             # (13,304 woorden) (Wido)

  - Kings
    /projects/calap/Reges.an               # (24,908 woorden) (Percy)
    /projects/calap/9a1.an  # ?

        hannes@jakob:~$ ll /projects/calap/Reges.an
        -r--r--r--   1 janet    calap     991979 jul  9  2009 /projects/calap/Reges.an
        hannes@jakob:~$ ll ~janet/word_grammar 
        -rw-r--r--   1 janet    staff       9489 mrt 26  2003 /home/janet/word_grammar

  - Psalms
    /projects/calap/P_Psalmi/P_Psalmi.an   # ? Psalms 1-25? or 30?

* Turgama project

  - Judges
    /home/wido/Judges/Judges_Syr/P_Judices.an ( == /projects/turgama/ri45/S/P_Judices.an)

  - Epistle of Baruch
    /projects/turgama/ApBar/P_EpBarB.an
    /projects/turgama/ApBar/P_EpBarA.an

  - Prayer of Manasseh
    /home/eep/synheb/Turgama/P_OrManA.an
    /home/eep/synheb/Turgama/P_OrManB.an

* BLC (Dirk Bakker, 
    /home/dirk/nomoos/Laws.an) (5,277 woorden)

        hannes@jakob:~$ ll ~dirk/nomoos/Laws.an*
        -r--r--r--   1 dirk     synvar    213405 okt 16 12:20 /home/dirk/nomoos/Laws.an
        -rw-r--r--   1 dirk     turgama   213402 nov 13  2008 /home/dirk/nomoos/Laws.an~

        hannes@jakob:~$ diff ~dirk/nomoos/Laws.an ~dirk/nomoos/Laws.an~
        1790c1790
        < 15,12 >KJH^                     ]>](NKJ[-H=
        ---
        > 15,12 >KJH^                     ]>](NKJ[/-H=
        2455c2455
        < 19,12 MSKNJN                    !M!](M]SKN[/JN
        ---
        > 19,12 MSKNJN                    ]M]SKN[/JN

* Efrem
  - Prose Refutations X, Mignon

        hannes@jakob:~$ ll ~mignon/eprx/*
        ...
        rw-r--r--   1 mignon   student   182789 jul 14  2015 /home/mignon/eprx/eprx.an
        ...
        rw-r--r--   1 mignon   student   180688 jul 14  2015 /home/mignon/eprx/lexicon
        rw-r--r--   1 mignon   student     1289 jul 14  2015 /home/mignon/eprx/Makefile
        rw-r--r--   1 mignon   student     4845 feb 20  2015 /home/mignon/eprx/psdef
        r--r--r--   1 mignon   student     6399 mrt  2  2015 /home/mignon/eprx/word_grammar

* Efrem Sermon on Jonah and Nineveh, Geert Jan
  - /home/geertjan/eprx/eprx.an

Data from other sources:

* BFBS New Testament (British Foreign Bible Society)
  - as part of SEDRA-III database (George Kiraz)
  - as part of Syromorph software
    syromorph/data/syriac/syromorph/all-ordered.txt (109,640 woorden)

* Peeters:
  - ~const/cur/peeters/incoming

List of an-files: ~const/cur/peeters/an-list

        hannes@jakob:~$ head ~const/cur/peeters/an-list 
        # *.an to use as source for the anzb
        # $1 == "C" { include in CALAP collection }
        # $1 == "T" { include in Turgama collection }
        ...
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
