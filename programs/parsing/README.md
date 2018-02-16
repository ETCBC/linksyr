# LinkSyr
This repository contains code that contributes to the LinkSyr project.

For now, it contains two parsers: SedraIII and SyrNT, both containing the text of the New Testament in Syriac with linguistic annotations. They should both reflect the annotated text of the Syriac New Testament according to the British and Foreign Bible Society's Edition, as annotated by the Way International (for more information, see G. Kiraz, 'Automatic Concordance Generation of Syriac Texts'. In *VI Symposium Syriacum 1992*, ed. R. Lavenant, Orientalia Christiana Analecta 247, Rome, 1994).

## Configuration file

Make sure to copy the linksyr.conf.sample to linksyr.conf, updated with the full paths to the data locations.

## SedraIII
The SEDRAIII database seems to be unavailable on the Sedra website. This version was taken from https://github.com/peshitta/sedrajs/tree/master/sedra.

Usage:
```
import sedra
nt = sedra.BFBS()
```

## SyrNT
This is the file that came shipped with the Syromorph software. The NT data seems almost identical with that of SEDRAIII, but lacks details like vocalized forms, glossary and etymology. It is however much easier to interpret.

Usage:
```
import syrnt
nt = syrnt.Syrnt()
```

## Transcription
Default transcription for both is the WIT transcription used at ETCBC. A different transcription can be specified at initialization (at this moment only `tosyr` or `None`:
```
nt1 = sedra.BFBS(sedra.tosyr)
nt2 = syrnt.Syrnt(syrnt.tosyr)
```
