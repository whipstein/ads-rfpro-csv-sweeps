"""Self-contained RFPro diagnostic-tools dropdown."""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import subprocess
import sys
import traceback
import types
import zlib
from pathlib import Path
from typing import Any, Sequence


# Edit this key to change the preselected dropdown operation.
DEFAULT_OPERATION = "duplicate_conditions"

_OPERATIONS = (
    (
        "duplicate_conditions",
        "Duplicate sweep-condition audit",
        "Expand every configured parameter instance and report conditions that "
        "evaluate to the same RFPro reference-unit values.",
        "diagnose_duplicate_sweep_conditions.py",
    ),
    (
        "analysis_reuse",
        "Analysis reuse and result mappings",
        "Report registered result IDs and paths, reuse hashes, reusable markers, "
        "flow state, and relevant solver-log evidence.",
        "diagnose_analysis_reuse.py",
    ),
    (
        "cache_inventory",
        "Reusable simulation-cache inventory",
        "Scan registered and historical RFPro result locations and distinguish "
        "active caches from orphaned reusable FEM data.",
        "find_reusable_simulation_caches.py",
    ),
    (
        "geometry_inspector",
        "Geometry and Mesh/Ports inspector",
        "Open the sweep-point inspector for regenerated geometry validation, "
        "saved Mesh/Ports viewing, PNG capture, and PDF reports.",
        "preview_sweep_geometries.py",
    ),
)

# BEGIN GENERATED EMBEDDED TOOLS
_EMBEDDED_TOOLS: dict[str, tuple[str, str, str]] = {
    'duplicate_conditions': (
        'diagnose_duplicate_sweep_conditions.py',
        'a77bb931d3d26f4e777f16c6e0ab5542f855e0a907d5d04829289fe6dd20e13d',
        (
            'c-rM!-H+SG5r5}jv0)!fCKO{ov_OSk0o6XY2JG|U?h>F-'
            '1ezzVbc`ud<&w6QtN!=S%zl&9$w~82pa%mM$=%uc{LSp_hGF=+tP6JY`nqkH_{{m9?VGah1nVC1j`2@<)#n{&T>~'
            '#T6Zwv_ecr-<9dFsXsf)5Jn>r1Go4$r2rC=@3i&;}w2PW2Sx$jt6i?ZNyjg-9ss$cebT?nAg+XJifuKdJ<4<D{I-'
            'CO>zp4V&s;RDQtm4U<ZQ(5$R<*mKDFL7>Div*wG6GygrP&Dg)$Lo$4Mu38S_;6d++lt#&P}<ZG{1FCnK}$+jgO+c'
            '2i+r%YE<0ERm<H+gO$+KN`h8WdQ8nAP>Gy)=Ra0+C(3WpY0Tg*L1CIKt3)W2!Dka&A2AHgyj_sPF+#IYxK!3{{_}'
            'LzCrMx-'
            '_4)2<lNg`}hR$Qb(7=}TxX`3C(vQ6LhEzdGm?vN{(29%{rf<V7(x3Grb`niO)x~8dwezD8D2T8Cy>_J7E*rEnT-s'
            'O9ImoROUAPD}zF2U-kX~9{+H#u-8*yjhX6!%OpbcS1LeXz_96}KklKwcq`Co&L-'
            '^Xl^T;)l0)+2U&P_Mf+JZnLY!yGwS#KuZ1T-Qw=$KeC(4x7pqMx0g4ItCu+7Mf#l2{yZ48_}lGx(2G9;)4-'
            '?FYALcBR4$@@+x*Pe-5e#2+3c^Z0<$ee*RJLPgTI!8c58-jBAgMk4Ojzzp^vE9sWw$AiN-'
            '6n*ao~d(<^#wB}8M+fG#ZyujGP60l1##Go~@+hP;Qq$XUc{UV<$^>s`6ymu=g$QFsUOny)doRCp^o7`0svK?#J6q'
            'otuGkIWg$>IE$dQV-'
            'U(Yg72hmA$X{w+R<YBKC*`zG;s(4)_<)dde1`^0LbBD{fetvv5S|I~FD^On(N5B9n;N8)Bc7?S@8Lj;sb&;$NhBS'
            '6TxV*VNes_|W_;)#q~RX-'
            '$N;ykpa@4lYG8F`H?#pHs#OCB(|{0P)HKAusEiinlogZG<SumGc2%URm$kR88JV5dnIvtY$JeB#n_o<XZg8nnP?y'
            'cZa<cHF3m_Sq|8azlIL#sAdyB5+g^p>qW=zK~xMGKqv5uy5?KT3asvT_q+w~WQ0&e)r|uLue20$W@LDdQLR>jzp&'
            '@&^WTvf7aq(iO8uEhIT_{CjMOF~dazj2LH^)NLLAcWDzWgR@hAVRCW8sK9Dp5wh{%BX2YE~L<W8{<QH=Up=M_0sW'
            'Ix1=SD*^}LgEmBb6c)~#L~4q!5{rZB(QT<9x$o7h?MXMOGdtprf8{2@e?Krd_bY(%^ro;h|S|y7|Mt+4>=*6vZE~'
            'oB-5#lCkPz;uPDX7$`5mE2ULI*4z!Oo$Jh+;d_Ay4!mgT{8#pyumoyw1Q3WOwq8g$oBpQplc-'
            ';a>^Sbx}m=BXUVNo3Wu<He@{(~f2Q1Bz`sGKQnOGct^&Dsk2^q&guOZpFLiHT)^xw7uL_dx-'
            'tVS&Jtpmbzi{ijq8%$ixFG51hUesn!d+bI}RSwbL7s7qh`X?tYLK?%1CC;e{a#<O~tXtFA-'
            'WzCv_<ePE}MOTr@Iyn-cO{kE>po}QWH91j&uXRL2?RH6Yu%zXCurH`z6~IiW3QLTNUYWj4u?@b9H6Rj{Jj^GTwBC'
            'y{Yw8&#yu>`C8aT-'
            'e$~VH;aME=jl%k@`+wS6pV@FvHOa+VsBN=|yqa45+j8^I%k0wO)$C5yV0KmPL#CI<$S}rilMJJ&Xp#oEBNa-RB<D'
            'oz6N^9)7=ZhYNQ(DcBz5$N53d?J7PF$sMb~h5##s$!rMOBVY6lT8<pRnQKIpCA!P1kT|*&Buu*yG9U7>_I{QrLe$'
            'n8*Tcin#O_GfY8EFo81uNcA!fCd@t1qd_}67F8qZp<_b&-|`5dPGwaGaD{_2a)$55&NfzuCe6c#Qi6dKpT70=PA-'
            'LlwCLAe^sU2KYy#FMy7{CAcXE#hl01$KDt9U#|4UkAwKQzP!?@%J(Udr3J4Y)1CH95-'
            'rQFLpb|8A}oAEel)bq@H=KtSdUc$C^#nJkYlR+B#kr~d1m_9vg<X|vy>~zy}mEFVn&{s~3SE>%@L-'
            'UNsA15|$dV59MQF)gh6iNWKZv7zjRq+k%rd4}FW<6C$OH$?b;mPm3qO5E8NOSpJe$MYjQ}x}{XG-'
            'z+5O#CBUEFl(M}ELE`<n~7w0a(G9be~AZ@a=`fouk;N_ky1Vi4=N#uEK(<*SkwoBY5lWd33-'
            's6P%QrEz14lVFVMZUY2a@;08PB_>OwOg6?MuTar>X6adm>XqNcFt%)f^_;TnMr!*P-'
            'Zr!QTtKc>ZM$ZpGMv{eoM>@6Ro9qDfS;*tw`2X06<GL6>uW}SZ3fvbWf)lXk0n31=!8kfi|Roq78Ro0*1SNhkt)T'
            'Sig%IxEOj^^YTd6qH)Sh2o!jWaM^Nb+vDb2P=HOt%M)2e=ge0P^?=qO&6-'
            'kQ05bFou<?a?!y359Q>_tM`8O86Y5*t!c9W%|lA9b(=IE8E;cgVof;P7gUqmrBDVDZ(HbIxJH3FkS{YFoL6Qzq~Y'
            'MQ%ddGuIWqRbyA<u_iUrldoy5&$Qp8yzUSMsgi_l$4E6(dq<jXkQESn2s+@&>-'
            '$=3Y)tB9k3?em%ul_~R>#C?&~4nLYo?5nF3bu&0L=zjGgAK#IK~apB*(Tb2>W1!>Engm4j)5<+=<=&D(WfJkvqs$'
            'nu~pl3bSA?>vVbUA$7ucP;h2Ds5vXuRFq($`j^hD{}Roykuv{3gIv7@cg_J)QSSPRJm*$@b&@I!JlmXb;Tpz2m8m'
            'V^WKxG?5d*h^EBd;~fg~MyVY29Vv@?=n%4X~ZxuS%GQU|MQ!8Lui?{SvvVX1tZ>NAA*^cZR7D6JU{Wo3aPVm6A@%'
            'q{OsNB!0ed{bb-2D~g+BN}@s#J-NoHI5w6(b%8@>`6ju?4mACa3(E{F&Txj5oC`ZDKuxMM1iV1-'
            '`0)j$~BA3F>I{*8j^-Ri<z@W<6s09gK;m7H@STY-'
            '424;Xx1khM)8oKX=9DamNo2E6<I@4w%gxtOoR1}9yO$Vedr#VdM3l*Bw;6ck61HDwvHFDH?NGCo_l@ebaJ9G0eU?'
            'mq1E=iLqPk_-08~bcViY5lF5_sQZ&xd1Q3`&V(O6&okL^O2{IFit;y)^kSYo-'
            'm`LCKsWv$16x!Bz<+RY>YtYL~IznPW!xoQn)>LoOE<JG``FEo9=#oF4J8v9U61tlZ+m3;Ov{MI@S~5w@pEIAX?f^'
            'd2a?Yf2*W!e*Qeeg&$Na~WGRp~%qhdsrG3xcRReU_x|C1R(b>Qu}lvU}ewcXl9`PcN&aZw|=wAHV!ZoYz59Rv9L#'
            'y>cq0P+RVk%I?l6V86+;`GxSOZFKEgDj9a)6fU}pX%Fwx69kZAWRv1HMoDGa7Lxm<7oVi&de?V^SWzGE~WDl_jvv'
            'fbqNSG6}bawg%p2+*sg@qz20W>K8vXkcKMgcpFe@P341=|$mXZn4z__}X7AlFq78gaEqSz89fswKyx=n^VJ;>aAD'
            'Z0rCgASs{oUo9?o3%XkOTqA^NKDijc*Du@c>o!Ca<b=5Sif}-'
            'mQXvpm%|jfYRr(doYJXdBw#VJE5kXVJ(!fdnl_01d##Bkt$0osJ89B3@E^`E`~woe5&GWS!VEcDe%@;IA{^^3b%m'
            '2SzFe*jLrlwMC@$(sybkyTjgb~lt&sHNaZN-'
            '<pW=TWUyIm&?R2p{>UDnCc@;I08&sL?_Ieni0pu#E|FllUhwbN`5H}X>a4*zvf6UueXGnIuSW3elhgX5ld^x)<_6'
            'rK4vTTKqc3Wucq}FMxjxaNmw5JU1}qfiYx-'
            'i9S#Wvd4oq_)@AXYVkbBq9?QS_`yj(KPi^50|h4z990JysLbuoFT<unm{A!a5wL*Vz-'
            '3~Gtcb{D$Co?kedL@AlS+{Bfz<P87grJ<Jj%}aY1&D^Dp)f31ZAM56Gjp<wRBmIJ2B45%m3>c~5qg?U^9T)?f4EK'
            'GN_ci#Sb9DfcI2I~8sVX|ELG|=@)!f4)jby56{Hr(0ziJWHasJgCW8E;<<W#in01v)0!fZRiUc0!M4p(Irc@vU$q'
            'k-4sz)Mly1wR^-%KLWL@_tz2i0<!J&$n1io5eb!CXt*q-&xh0t`oRjMz;*J3=>_LWvI?93#FP!w{h?vl=|z2'
        ),
    ),
    'analysis_reuse': (
        'diagnose_analysis_reuse.py',
        '1bc0144e67d391d52af864a8ee25bbf55297a08deb7ece8968c84e39c2a0587d',
        (
            'c-oy=TT|Oe7Jm1y=+Qo`G-'
            'C^rr!7}JTP|=CS0%t=lC3R<QVFSTYognzTLcRD@AI9$=w=(J%}a3ix!?Q9ahywD7L{a|A1|tcg?X4hh(t_eF{!wy'
            'Q^~ThER%dAa2K<ZSCgp7<3uJ!&MICD&iGvt^E~4IXmnZUOl}i_n=qafdHTRaR3)WkNiG1Tx%g};SzK_z@<K8Z-'
            'f<vtR#wHIJd$G;ZNq%SM|5W8!68UW&P0;cX-'
            'M30R#Z$Db+lzh)OC__;j=3uR^O&cWG+T!D7R3c;y55}dCUYa!wM83;<_p_a8K@t!8$E|vN#Dhc_CyH2__0g=t})4'
            'jJA9PL2px@X@aBzEV71BJoZP9<BUd%U=XZpSywy=Sdu9dhdF???4yxAt2U5BaQnOB8k<<A$*o1bz)yW4AIKZ_e4a'
            'my*^2*FlLJPh(LdM%zR^DTx#hVw_&)_B&#bg7q9V(*G9(W;3DRU!XFQj}ADu2f&cA)R3g&0?FaKLDSHao*>w?V~6'
            'th=f&OZfT=T|46gD=ak%PU;IKOT*O%f+|VLS0_WudWuCXSk@i4}K*a<Bk~qRSpHslXW9BQCcBNLK$tJ_<bVO>Bq&'
            '_C&ysKNvtEKjv~(ErzF1%Q=ADH6STrxSmNnNlBT$kysGL_KFKPK_-'
            'z>daK@Sn_m`i}&My}y^VMQJ@<`hMd|O^FPJ@&A$>#-'
            '${CNd|wV1A>V|yEltut2UcO74y`RdH`#vQ;A@qk3Be(<V+=2<L)SmZ}B7s)0+@-'
            '1Ko7h1BSR1t9y&)oa>SvtVn@FL@~dN_!x|MNvCJD4WTkdb9A8&t%{@$vDyBXjHP+ZN06I)G-'
            'cJ9sd$35AYbHI`+P78}QKcu|43!Xf|Re;x;~B4k{MaKnvNUxM`C4q86QZIK5}==t(qzD4d`3=gRs^L11Hf;@y6uC'
            'd#c(%xf}-&u-mxfZgznVKL+!O0n&xP;-cHA*D?1-IGy>T9A<NE7vL46}8T$ARV8<26<^rbxI-'
            'vBi;Qs3^d>`{nc$OtMzVt8O%w5;aVaUI-tVWPDLoMddnFx5G##ccxERiK)KI5FG@BSR=jDk|*IB%H}{Zh1LVUE${'
            'DPS{u&2Tl%+l=0+p-NCbYVp4*0{YLw6BcVUvM#J3_%nX^ObH-=ns{6C8%S1u7=52XENd^dE`^^VuzC4R5ndt)t-'
            'a!Z}fX6)VcRjS7t^{^$J6_;#(D?mu8o-'
            'vtNx4&kL14gh>uDWWVtGQbh1%i&!MTJ_NL@L6^?6xRU6Xy<1ElM$(5p<<4D`fs(bs`c8KjD`^I|F(Jz0u=qSgm43'
            '&cO}P#Kl*=x?`nBXu#7cQ!=n498-(B<DQSmrrE;P38lcs%{4{Y-fr@2^iu*-'
            'O$zL&)X{Q`B+e52K<{dETGnOCukF1_@|(Ttr=gIV#nBp0z{CNJ95zsm^+#U(%o%uN9!OB0Y7BHmoU9+H$pSrVtzd'
            '<lz9<5+{aObP<_C1<P^t=WJ+PTFRL??9Gtk)D-'
            'GO#cfyOdphJ<Y@4*jjc92@9EEb<I~xLzCbtyn(4mpqSMp(Z|e2X~Vex9Hz>u5bKb(YJJDu2qa<=!4)by?%{Rqm$g'
            'WvC%IwRI`%2=FK6xV;@37JZP<m(7YVbfeR17Klx_n)N(!f7ZQh4W{MdGjWR`_aN3%|?<0<Z?tG<^mxV&Z_SrP!Ip'
            '%n>hFdC^Uay@GQBkLQv?Bgf_NdUGe|K&??`35&n%1=Adw>*qJ_02v-'
            '981CH@GB=lAgXO(?qI39YDgiyOX3ZcvwYSmk?U;o32BQNN-'
            'Z!z+O*u?pbwB9k56yeS;`W)4;qB0xCo99aYS>4MSngw&!C*jhb<b<RZjKTB1qyQlEN^r>II!orkuN>X0`cUa0@*$'
            '+hca!)Dz@X0CCi=U633aUEfYgzw0!K&a3=jxEyAKbOsT5a^nwUsEp6&|m`8l{)2SV6cGZCl$XzojXG@){Ie<Ff<~'
            'Tx^#Sf>f1(qu70|fu6CH<QmVIUJA(M_3vp#`HE44jBrzdSO>+&C4VO&^TQz{o7_muKxW4g*H1vzI8~$p-'
            'BjeGP=k;pH%X|oPz{%7|^RNq=H~0%;8`yasAJ9ONRBpuF-h1tv7TUgg(E{xQ-ZS+^BesJPszqaR>gmr1;ON21yTJ'
            'C3E1VCJTFKd_D(aFgPrInC{Xfwyrn1-'
            'Y$pN6yiT*>x)WmU6i5B>6B==Ig2rC#0FBB$za$Yi?ljErFs`_Aq*)J{Jiog~cYKPiMk*|{t+I`F#1X{Dm5K%zxA+'
            'UyKUT3$wI$t+3EG^{Q2-'
            '{F3!ZdB}5!ONs2(}|7?I3idQ9r2)j9O}tRA&qG@?Wkm3Lz3IVzTJWkd7)2zJ#TIB(jMjAMM+E$@QF3J5&$3x3Mu%'
            'JD%_F`y=X}GLQTUB{I6*LOB6MZ7F>Oq3`d}qp6sA-V5AMF-'
            ';{=e}koC^#77#8;XXa3g2b?7AdTyv<2>XB_Kv$0IFb?qb@VV&+=9ZYcv|^yZvepV<b@1kveKGPX!v3ilSao_MSaN'
            'SO07$!%dVOb?DjZNXWyAImEx@8^jqc35Ge{ME0P_t8g|AQZH}<%uPA<t7COc`=G%Q)qeF(8|$GKEr25fIV~J_8MM'
            '8;r#q<iZE>wg-q84<{$d~49wVAj;@_=P^>_<%I}fdPl<Fw)+l;Bwp}?-'
            'Yi?EySbG2uSJviN+SO?KM;*b2K*&{zHb)KjFAQ^<hv$IQtv5r4YVJ5xy!=5&84fTW<2Do`cbg??`Jo}bRa$`v!Ps'
            '~gV2mY3ien&!`M}xXU7}HQ`9#-^HOY%c+#Lnb&klmtrw>?_IU53NyTd|z(EGk-hqyS)=us0*aANi`z;LnFaMv)KH'
            '_8n=xn?fqB_h9tA_G0SwG1aW3p0cd7js<=jz^@}wXp-'
            '}LG5p*vl=fxSFEh4R#OWZ=!0x~E%d_R#r>Xh+FhMBOzP)Oco~XG{aTS=l)@xpM)>%7Krbh1N+lRLa)AMpyGEro_B'
            'ar=oqWQ&z{i;D*w}v(C<aG%Vep_6;_JL6$f}0NsF8;ckHs2=H_JBR97KKWrIu*SF?Dr4<jP^n$-'
            'nUu@by(3{Zvp0p@`bu-Rg1a)!~`qM985JOZ47tj+ucuDgO69e(Lu5B!#HmAah-PEh0X_!Lr|RU-'
            'H^RV1SzUtouERa@eF?2r8oG(qA51E9kV*ui=CNeqphzFiJdlo6H*3zCsvo3_bb{2DSI8IVV%RhRm%yp0d4Q>^3Kr'
            'l8p7>&qoz(FHs1~RyqyhW*90u9g=Dv!m4!%XQDn2gJVhJoCdM*^;~V3ueO)$0aJ@H3jWYU!nwm0o-'
            'D{#}Hdu}8NmOsDFYHIl))M_E>Z|YOapxoF9&=KD(Mm+E)`NidyG{_0C4#`w8Y;7RqrU+cda{H'
        ),
    ),
    'cache_inventory': (
        'find_reusable_simulation_caches.py',
        'f34c620360c1f45952b3b94ec0348e07f4c09f6530a0a1141e61adc17d4f06ba',
        (
            'c-'
            'oa%TW{Mq7Jk>S;AkHzVH~A9kHLBYV<uS?=%hi?4zS1u0%OrOCo<(FsU)5>|9#Inyy#*%>E@xeNS^z5E@Yaf7gANM'
            'Rr0^BVAmH{x?vaRzcVdbBiNEJH^MLuCzj22$F*Q~Bev{G+6^38OJju=729#UF-'
            '4MGw+aqO1ADwWX;i&uW~t@QGO3KLynupzQ?+~$z?X^VUEOGI8@&gjWvh*R6wC;&mz!B4K)zFg>81fLhV8Ue7DS3?'
            'zO=x<QA<&<>rNN0c)d4x5|tv|8@=0bC90&+473Aba>?sx9asgrDJxeJ=#2n7xfS)kNYXS-'
            'l9g_@tSncpZM7&%CbzprTVSjj%dKpbNs_Rp*FbDU_->4&MpbHgA4sp@({0%OPO5cSU#R_z-3W*T7?mW+-'
            '`II2ExH_H@w5@j`R{{a=;#~gSqRLQ0z?XdD1#=g+bviGG5PKMV)5<s*K%>W`26piPdDY|;`ehlXJA>_y7_f+Szdq'
            'n@^xbQYH@vj`L+Cf{>S;}8`%E^)T+cPdbw15D@?Z2&7Wdv&(MUNo&1y4;O1Ln_1#&*;7<#1o?^I?Aw|ws5DWYT$Y'
            '7qja7=|M9Mk;H3tIt1%OG(eYeqcI81N;ru;c_12hev~&z#Q46+@5Fj-'
            'w(~xdd;6gRR_(bFCYlrC$Mn05^oDOA*fpoUbegYy%?}wNE?ts9fai7f2{rJ(AnW{)5-'
            '8mps_Tzg4;j_<lhKKj~LiHNp^6@eE!s*y54Pn%~zVs&vNE15Q7)bjH%+&qgW=iOB~?x-'
            'TEQagc5gq6SeC&n~=o!2`7j+}V82{(kl@*N=|$xF^yZVc9gQ0a672lamnk_ndLW3AqQJYV?-Z@-'
            'I=9n8F$Ub4KY)Xam#@;N6%4PZUVD<VIv+f!`aVNBHB9JP#5op#fE;f$S}@#5p?wRx7!Na#PVF;d@3qMsC}hs!qAq'
            'O}i_dN^!p{%CrN<hI(>~YTvn2Sjm+wYw;**I06-'
            'QmXJkw#+d}A@7GP!m{_Id5=s$OVQ}*kuOC>ud*Zrcu8?g+S9!HCZEYDTSWpf1Xc*fyMgxk^Mu+kOq(gy&exx%O9%'
            's1~&lWNqeLCqC)H6-<0uIPs7IU&A?ukdU=1zRK??^-qL<eq-'
            'q*#6%1;ioNZh^vm8{<voj+BDLA2YklClzswf)Yl&S)vBHo4O(eeuMZ?ZSoNz1zA6Vy4v3*4=Pb~IpQ=x14`1KtF_'
            '1m2+BLv+&Y**Ox#z$0ET^cU|9X`VQP37yQ0U!g9JDFje*)YLB(V-k9t{3t%$%Mk$vqr`KhOpFnQom0KW1C9h)-'
            'uL(qmB!V-'
            'Q_A=z^MAan<85`6}2melfQB>E0?e|e3rLnh@)*3|E!mW5u|&3%>@B&ondX?_69NIUi?3BDZ{DN33<AA+cWQ~J1cw'
            '5%`N>iwuUIc2=@P7`zc%UwJqo|gjVkx$qK2$Vy5^sH2^=%Zo4jJiJi31*N=7`av{i)x1x<AY*bnX)n}eMi)fI?5x'
            '=z%V8%+Bd}`_8=HWX6!-i=QZEnSDd-'
            '3JJlXyWv4;agHx(U&>Lo4m#3jn`Vr>cn$1SAcD4GlQNAYlL8c2V%sT+;EFYJQ3jon&V=tOkRjzKVAQu37CvM0_4l'
            'dBcnc|GSMCPx4yy=bqfb>aMyjk^JZuF8D*c{L2+@%^hHS_f?z}71toy@X${m8wtj;<S?z@RuHAevrB=Wb#{as7gQ'
            '`mImW^_zd;E(~Gs(L2B#<$zH=;1Pl`<^6D|ck$`fc(e~Eud&bbG5I%F0lO=fftUd}Jbf<|L>ka`ydC-'
            'g{YM>9EbV&TTi_Vxvtv3j3p4hD$6wiZDw6XT!W}zhA9@w_Lyq}?^)t&~CkEkF`aMFa$05{~Q&){nW0f56OGiU<GH'
            '}A7dk>Pw!+i-}$MX7-'
            'w!?*WaufaLZo{gdKD~Q}DF?|pS@(us?+s#;iv2vtAu$_p?jkv<t|y_(&NSIXSSh50bN0Qb%lu`)VjM+`ppQQ}=Ev'
            'hdihZE|e`7z6`%MdXa=jlV8|yz)xYr50;g%jCdJuu!n~uWk0l#mmJ9#>O*@)bx!t<IA?!c2c^5!t;G=3D?3d<{QI'
            'n4jQP{0fYR~Q=qji_Oa!WWcKxbP<Inqf)LB4vD+$l%vwug~F20Yn^I8UPmmqZSw5Q;JKxo9+10H#}O@c)bq?7M}A'
            'J?R21m0MauF6x#Wbr>==du7jtoH0dT`C%oWQ746B=?#c-lO0bwi#hXvwQr~2PUYlSLr}X2*-'
            'TnCF#EnTOZa4>acE1yIyyQ(Y9=!4N42{v6fzuvT^Q7E7Zrnfy@uWr6!38uz${#;~(x)}lBAl(s`=>Q;75H9vlHhK'
            'Rck*y0_k8lmxO><dTtL`A*vIj#(|bD@yCl4o-3z9~n&Z1p5eqX-'
            'fKiUe?-uR^KZx0GEQ?HFdolsMS?=*qY<Idz2J>N<h~m>1ohjT))RlWVne}`U&N;qKYj-'
            'WS4M*iZi!cFwq0ekcGH$~_d>h?*HGIJs^zY1bUke)_T)G(uDPe-fdH&X4cHOlhjx``?`XyxG#{$=9aUFGeYoPKE0'
            'JEv)M&`{XL=12>>!<zXJRjsAPVv2|9jhRKx1>kNvc%hOT9$~Zvh-IM0$85>4_VTilm'
        ),
    ),
    'geometry_inspector': (
        'preview_sweep_geometries.py',
        'fd94cec8f93f5ebf3930117b2fd720ee4bca7409373872d1b0805a4550a3421f',
        (
            'c-'
            'rl~+jbk*l_>houc(yI*hX0(M9FcwLz&K|CCb)lT_};ZcUopwia>#^7J!0LfGCE|G4@BCZ#W;ezvRrzx?idal$3PN'
            'NxDZO7S?sHx#pVpnWpKp#kyP-'
            '<8}4EoLwi&Rr$Uuuab+ho|o&@by6%QNmINpC&`Plxx9Z|uhvb{T$SZAS(VLZ27gtH<jvFLRXy6-'
            'd9zt0>&psSj91li4L>#2q=ZjpQZGx<4koGpvmCES$+LA*eptd34K-'
            '=X8GJ4$JH?`yT{l(pWs@ulTv_s$zbuPY0ZS@ZC*^OOaxpHOzx-vG6wBqTDx0KUl*zKL7VD&d|4-'
            'J{9A>R?)E(ZNoODP#T9s2+{Uvmy6~R1e!?^uX^0ZzhO+CYXkL$&xT37V~cDmjf7mK8rHFYwpiwTVdI{=`lfjnR_n'
            '8dg*>!hjXn^{2v?i8ys8L!F$Ha$#WTO0h}34nn<z#3}U!Ro4N%4A+os%ceD0LrHb&Q*0$0hr{zb`^Y*X}!W3ngmC'
            'O+1K?7R&;e)E(pqSCQIm0uXe_>x+$Acg5!w;gSo47z=t&=!=wfPE$TJxiTcWu+ey=OXJ@*q=SiMVH|x!+%=4t06C'
            '{cS^bs4}k>6Gqu)wC2e_yWWGx_fd7QL?PStCEpi}j`acdfpzROe=M4hsPcP`@?T>YsS@ys}BLF2(={*rQyU`ot}k'
            'FcIum{(6k_(huwFWwp4F-'
            'wzkpL%>x4%lWJvCNBW#;MZXyF>z;S=ZoYBkc4rcAT7}WZ^Q}1c3jWrh%jRU5KP|S5nXKN<zn58cAgwPJ^bnUX@2<'
            'f@cExlo}J_`4__Q52MIu0{`Bv!UcJaqU*$*t>-'
            '6a5=?VP!6mYSG*<WtvaBN9EO(uXBfOW+bQ320vQjV)RA_`p(K#t`2$x{R0i`k~6OT3xuMZ7sWe)Z-'
            'wKR$c|i#R=clRr6n{OrZy^ZfYv;o~Em`Rkqh*~^pTqsOPO-azvoo}HY&`E!1Fdiv(s_dlJ|!t>P>&M7Bqk;@5lg?'
            '~-DlfO7R`7!_T@a2=|N9}{m;X>t;s#(s8>--YHI4hz5&d&c-'
            'M>>F$`)j#4I9+YZY==H2Cph)bxWoOO1pWhP`wA#UiJQhtC&>#FGy(<PX@uaWDObDGVvLBeDuFOIa888QBf@?hPhG'
            'lv0sp(7H0u?8r;+v%ap+I6ZvMU3nve0Y>@^digeB{X4hVH#Eoeyzp)FEDxg&v_##(Vmfc~WXun)(*rjN3j``sAY{'
            'fQA~KUr^<v+}Km@Gu#TMrWPdd%cD$ftOV8?i^`KLx7)D#l@m-*44O4-j#4^iW%+(u@-'
            'R|mbFCUC>|1cQ&!H2(1S3hj~f2VYkY?CX*GjGp<7O0XB!})#@FP(fIcrucbxpHXmUZN_mgv=RMeteysuXE0&g$1k'
            'd#(5>4L)#;y%17k;WVs7dDC#M(*;RT~QM__zR7l^%9o`*P5RnzzYTmT=fh0(Dx0Tl1EsHb((vIJJ#Sj6dKcDIZ{a'
            '<K;vRbWWQXk>J@ciT18j|_hi%Lv*Ns*89#M_1RqU$GvCmYX~Tn_Ro<g`Q6(tgc8%-'
            'z<;s3`aV8B1{pjYnbGbp|bG=zFH){iD<TX>M&i@TvhuHs2;JX0aW&RHC32)X0>171NHjCnYQO)p80o*AXMA+>?^='
            '$DT5U^fdD`=e*Q{Wc(jY`hTH5~l{nV4yHu|XIyts}%}4ED|hZDZUg!HRkC5iRrc>s%n22_^V2bkEa*Sk*MJzFZNd'
            'YOHArb@rMPD0{TuEP#I)UzU@cmk0;0TGHXEmIkr$8*qzqDmIz}3F6rYz@|=z9y!gD-'
            'S6BTi{s{_!T%r~gXe!z!Ql#;JCx`QFEEZg@&K!P)0LdM10)9r)?%#Yd{S^x7h;+n=PRM3+N+6?v<liRZLR0&?z<C'
            'EkAbzQfw5e<{mg2Ca0)bv!pH>?|2|T;FR7T3#oY=4KsUgPYc^1WW&N+=6Mo@;B*w&h+18gJmCQE{u(O*rJ!q0W6t'
            'A@<F2Igg<w{>clpJz-'
            '5A_9Pwh9&vR{=RAyeG!%gU1P{xGvy{3ouWE;A=UguiRokvb*69;e$qOSm?hYNh#!R<Q4#>miW)b_*%T<c$)la4e|'
            'wWt4zO(S$(1R%Zmn*bdb!dX037O0)AMpR|8|!!=!_S942qi7`OPp0XguTi^cUo-6K4F-'
            'm`r{5#8isG7GWk(+Ji9dl_(7jlj*FmZ>JvXE%daq5QOmCn!?r4Bzm4aEzhzs~2!!EL8AIv00!5+|UW)67~53hy^q'
            'Ot~UK+n(+Bg*%<t-'
            '8d#lcm>ip@y%Qq0l1A|6sL9#RCp>WA<VgLI|F+KI#MUUs=gg!I=(yl<+LsUpiFYI$jey^RgTAWPmxFXxEjAz0%%j'
            '8b!})I?#^<A^PD6v>Gm>6ai?1K1e&65Vhe>_aj3%>Ly!WJ7LAx|O^|&6_#b|O3|K<@^1*$cKFmQxi<Y1cqv}iU<!'
            'O*@2mRAhFpWK+U-'
            'KGj?vwDm#VE|+v(@!wOe<+kcY~JB4^x9CTWL4MeW{9!|zBI*Zd`WVL&><Z@Ik|uIg7_qCr%|4yujA_znD7sy*Xze'
            '12T0|?Yy9KT#EjR^tMgT{x_-8p);p#of-'
            ')pvY&#+d&Sga+bcIY1UZ1zPuQNn<gL5e+lU%mE9%we+x%>E^wPYam(Fyg}0clA_EPkR)Jjh1k$APAK<%cm!Yp+h|'
            'Al;$VrPt3h502Lfpl)u*>T3KTsjcjr+4~eA#B*uisSlLQTpDeb4&rx!(GvPiYOl*5B)M<47K@|v!*w+zL;)<#vmf'
            'ENf%QfF8<##h=AOrDg|IqjKzmmv2(Z_{X`P8xA-'
            'd0aB3>4pfQzN0nO;dVFsKPE!tCpV#ao5hTrNS}O>Be+rf(|11YRHJ=Nup#T?p2+vDAfoXUEs;w5`8_kSX31J^+*k'
            '>Fd+{_3<HU!A_sPdh-JQ@zW2_UgpP#r$45{1b;TaWH#pyL#?iHoVpo_;YaY=4cw_<pfnr7t6i-'
            'J&=djJl*`N$1ZX^;-'
            'w&PwwKXw70VsL_4gClll5T(Bq*vD6(H%x0G2;IYvJfpWTZ$DGv)Oquen%^Akd7J0Hl({epci0OPOA?Yzq{p!a=cl'
            'ixB?wi6aCdCRJiQ|EeEg-+_i2g(5|uYTs9?gFq+j@Nc-raBW<-'
            'q66_sFYNf{D32Z6n9K`;2%(N{_Sm_k87PjJ`NBZOO(b37Pr}>j-'
            'Z&F1Hj4lS21s6e}G1_N5NI6Hv>Saxjjyoqjb8lY#`0B-xo>8~&HKA@U(T*Qf6wI-)|8U7OqN@t$V-'
            'Mcrv62J@|L0>~tZ@xY$zo$6H$GL?Jc!}|Oh5@-vbBP0;qJA4c)PLt($Uu}zIy~2sXUm2HJ7-$nAPV4<GN-'
            '(xq!V<@7R@ft}eCR4vMTVye!A>m?H;1R=%0$(wGku50XKV&dmOBtZM|$G=<+cs|MIIU=DG!x2c6ZHcSQEge><A$x'
            'Hg{0yx0Yf7ZZKiIFp6_Qfj88Stj*U{SNKRPus6R+N9$*CI8TSIJx67@Pgw>NdG5Se}^Ho5dt4HtQN-3-'
            '9l2c0Kxaks5;u&Js3iJe9Y<E>6TA_i;BjVt2P@-xTdnY};$@3w;-'
            'I%cJFWg7N}!x8(=mZ>9bi&A~ur*QkNmky;R9wFwf)Y?Fwg*lbse?(kgV>TD~o?0BdyR6qxY`ERt^ENs=%+jKUWq@'
            '<uVSC*X(ZPdhLJ|N?n^MlZ8v$m6TJ$8dN;GgqZP*dwBByhH+eI<hO&f|JBlWZ`V#aQaG@P!T=&Ys2t(TAlC`b#K0'
            '4Q5@7y8ze{APq-vP(9}T7R=2EC0Mhbz;=^+iT)b~7YqnCZUz>MoGPSEaTsi22*c1oFG%k`eD!q8tPM^!xl3QmJ7Y'
            'm;n4E8rME|y_P|eM3C;A4U8C)ol?TeCHnm)vFw({ilDqocwyeNi9&oa1gzIuZ#`S$GAR|^tc$#&0!iQA`s;%isH='
            'XzP9B9bYcmL)BumzHTJ04Aax(f^?7uNSIWAe00JNVG)1b1AR_iA`KL4qoEyTDf{8sdFT-UD_9FgU&aoADO_S*O#z'
            '7gQ5&+svDb215!9LPQt|QkZk=+H30@iS@d5ULd%Y8?2~Mv?48rsJa_p4<CIZGGvy$-'
            'mTP3<28s<b8yi|<PwSyD#nuZM%Nw#Tj*a-kgcZv>KI`32$-'
            'xWkrqbEY_Btf#nUiaMkH;}OqEX6Hj9{D9NS8$;m6<RG>Z%9sKu?~Xz#xB4iLr8j{N?b^&ktWd$yKAwWzx(U$h_sP'
            'U1%L{(t0`t3@^(CE_Plm&`%=0b$H8;yF~ZtWu1rx;hLQ_B9<t_3Q^#TRk6IpmtHtdIoFAXd|qr8z;O`v7e<c;-'
            'aSC1NA?Ako;oo4xJ=Z(&}*n1*`tf|e-'
            'Fe_h)%6iEj32_c2nZxtGZcYEF&%Yj@6sS#|_zu&r1LJR{nqjfb(Qq5|c#}<F|DnwZKz!jhbCs;+)uneY%mgsI8z>'
            'tNv}+keENzfW^OKBafE#Qh|W)d?qa&!a3_8(MT189ohMeb;&cKrKn>Oxa}N`(u(&bOvXVlVH&E%%C}NkhLN9b2Es'
            'LrED`ill5~fL@_lo1V*WL|FEuODv5W^Tn-LG1or%fdKqtxuX3aHBl<N&m3!ivG8UY|1UZ-UZqF-8{&-'
            '7Glfh{LSl5z@oC19XLtzHYwv^a}I;f}>AIrHkd$)P4fY^Ld<*imvLMG1BP%MSqcQF5rrja<@xfX3WQknS-jMoY;Y'
            'Lg8v{oI`r+of=td`FIsKI4kAoh`|r`J4f9++i8bHdID%4c9$awvT2gtU3u(Xz=!}rNj>As8bziE?jgGg_X1v*kHb'
            'QH9NdNhwr@jV3*HEKL0K;r>e&KhohM|4m5LgEGKYZj$Ym0RGMgb~dbTd-'
            '`b^lWsKrjYBjk3ZJe`tf((^AhT1sTzH$Kw7^`CqCpN7b0+jGS_+b^-'
            'YIJ`l8Ku`!DBZD^smQ~){b`T>4lMu>G>3CD-'
            'C>{>9_n&RHBVmC?F3?2^F;X%rD5othgoZL<8&mlKoeuG_M|@ap=H;pyv-_Q4d17Z@I3H;@eb3H#srV(8FOD*2&ge'
            '1>#P3<FUX50Z8y2kxnWsThf{5K0ui=g}2rW(9JEa$<@DOFk!U6r^JR|Ujct(V~s@^U&hwUnVEut8WyKU*_8e-'
            'VBJE*Wlb7PCMRBeI~Qor({z}oWYLgDY@_O+@b(&HGXWDYE0W-'
            'Ya9l+eOI6Uv4a@o%}sSr;r210{2{B}B~G<a4h486qb?G)7l$)`SHi)&efW@v5AbtAxCCSEvb5PVma_{T#i<;Etig'
            'B)Wvdw>diD&Cjcg4e(U6YkjLe>j8S#OaOym9z4|cn`U;m{FiK8P|ZT<Al_*Ob@#1y(MAnsV9u<X8fyvOG;6sU!h~'
            'q*dlp)m+lv-xFFC$ik2o{)$^PD?Y_<nK+u5eKT7krFwmjt8Ib3>KqdVPt4M^BH^iBKcYLq^rQDF2Eo=(TB8<i?GM'
            '`S2(aN*I(FYi?~n<cBw!t%-?Jr7FUaup*TRD%mRS|HL|u1<kRRN+2*pi!IzIpI=g<*F@TNX7Y#q;-'
            '`Sy6^4WHUin6=|gktNlA|(fIPGl32Re*K~x5g21I;{OA(VBKA-BD8EWcsW-'
            'N)>qLQ`u&>tqIHYm7)lxAyK*~ONO5WE;0HHDu?BWa3W{7d559Q2nGN&vrI7I~V=?I$-'
            'j0D;eaaErPT<S#Z09M1?Pkc^Kjr_dJErn~148jiXawJMio0hp^%S;{pdUuLn_sTVgYCKDDstOn+D*2-'
            '`Mp&ohSKH1iXfjtlDkl66FK~b^;1Sa)wc~*@V)d8V<H>CM-z^(|Y+fYv>4Z5a%$Gc)Jwm>$))a=7e*Ui0-'
            '!~=xxpi~-!7e)x%u@atF?$U$q+u%V8U<lq?&G(kh@+=D<K6x1s@zQUFqFj;V(1sL8U#I*P-'
            'N>Aw6$fO^p(5)>AiPXA<MrSxvHi?>E!9&TaM#BF=rEsw9rJWx0Or63&w=<~e}noE?H;&#V>3H(tmii*dWiZ}3ExY'
            '@xBLK^2p%pQ1{>QK_rQ6Wf?d2rI`EGz*pbiSK=ADyS3k2}cJZusYO%bB*-~LG?blrb+7^uYqu_R+-'
            'Ey7VSkVmRBQL`y&4<24J=l;1YH-6+u05!Z3LuRkvpW_iM&CvZyjv+}Hj84}T-'
            'N3irEm~XB$`Xc)zMlf)p)Jwl31{g4<dar>#+1kwks*k(*e-`u;NqokSfnx0S}?ak?gUdn-'
            'a!MWFZ(_$bqO1uwp&25=o>1bf@0~ma^)`*rZ`aWqp$27puUSTIw{>Jaa7N;;3&}V`czA>KJ?|sm<L=<@0hmlh52z'
            '-*fvs&kMlyYEi25-gi!N7>JJxImV-'
            '!9Yi`tbrUGSgv&{U(=aWJ0x^vn9|#z2!5U2+rE&)#;O%7u#C>kLW*U%$1wS=_sYcR%a0Z9q-'
            'kh!xjjqlO9h$?AENzdl9&}&A&O-'
            '|x5ROe4spNj)$uUXJ%PF~I>pTaFKPPphbv}27y?2x?XCQPSEYs=0=*^Pswn9%4u&6M9L{QRni1&}iY})_2SY4Dl9'
            'Q62c33$sRvu~9E$M~{XTnLpT?@7S`<2rzUYO0GxZsDs`gt)tg3!h`BSA~)do2Nh`p3oR40A!&c@%6S!Qxcvu+rp<'
            'IYN0WVBdGZyFdaTQNgnP!{6oT1?jj~Q780#dB#6NObZl~vjVzB6f@N`yzBL+l8f5&Fr8*KAA&yIT;-'
            '&~@{)y+*>u~i?7G$kKKMJ5?Ga+~?v}1%**##Vs@*)6|;e8B5Y6Tr+YlGByJ;L}hv_YtBIGYvPl6~Tnv);W4y&eun'
            '<M0JL4r5?xBj1$8#HL0R0Z2-j^O98K04jJqWEh};tN@Rv-Ophim-WO)qmjAwn8x4227AQMa=+AhK1W-'
            'mG937qgSTrDc%f3cxwWXV#VEPT2yFo|>=a^u%u0AJBBD`;<#j5oSiX!d^(f_hxxSX8nK~4)v$xnD_amB^Cn7f=XU'
            'NjSb%G&zYhovOE$U+FMOBS*dUM!xF-'
            '44J%Gb4ed_FDv6yldLGQC`ziF(jCXLCNU*5oy&uS#vQma&`B>;9ukq~|M}wTx<biP=1-BIX{b1ZXl7&v7-'
            '~lqf!?^+s@t1sKxW@IXvuGundeHtD`x3J?oxoRlor1M6FM+sV4+sOJ7C6l%p6$=AtIjLb$9!hKOLNY8=zQmq8W><'
            'WyL%lf;bOgGmXJ?DRLq*1^lf5d8i9b;#WBqZJ|$_WI}%CR}0Rb!Rw%1mBFgG=XdGWIFq*R<z}4qE7vpO_{$yiVhV'
            'mA}KTtLA6?vGrY*Blv;0yfg8ZxNoJxQZdIM!?%uH`$YV=cs4Dgp<F8&bL7m@G~dTRm{%tJPN(S)9z4lGKA8d_(E='
            '-7&kbXGHSvaHH!(dJ?137NR9rtMIq`WJ1Jc~&m&@yCi}xXrD{xz5wYxB2L%|$ay*O}(BJCU}`5q9ohBn>!>vL44!'
            '66!`$+=xDAlm+dY9!%NXrGVx6&EX$v@9uAgqTEQH+t_P?JGndguEc(l<!WHG|VX>BDCi9WHT!T!TxJq&yg>nC>zw'
            '@(e)I0#(c^9<g&gJ#CTcYqb?a*@p{`?^|Tg*?;x!L1~=C+y4X}B?tRRye#WI{UcXTTb4y$^+IWMBSdk;llOyS}1q'
            'V$Oc;E|vP^<lj>EX6>0{XhpHF6%9<6|>(XQ%ZMcQA3ZYf35lz>UFp22#cto=KQya9UuNCHzZx4%n`1QjjStOhO1q'
            '^?JSAtgmNfBCfFMtaP<PT|9bVU{bF2wPkn~YNl{D2)U3@#1H+>OV6zPFYNHb_jM*>>EeD8&Qt<8f&w9Y#4i?vluO'
            '?hz{2#9Fl2SU0bWAhM+8c7QJ|$7z$o%N3WvO12{|GUkuVUke8<I$)k<P%7V#gLa@;U^gU&H%v!K7TF0lNz&TGnCl'
            'dHGIacM)U;J(xF_6j^Xxvb9XckmL+tu<?ueCw+P5C(OI$>V$X5}v0$_@xoUS>Z3w=(nTbyM_<Zj!tw|V7Ra0#v_O'
            '8`Le4qOosw7M!vpYmXWa~6s*C!7DWSo#KKGn#IT6C2Gv<yB@2B{VG#~!zeq5d44oUWf+BO6ef4XR?PyV!DyB%G0`'
            '99BMb~*Zyyfhd0&5FW<+7U&|2yD<X*eUQ!5kVHq6$17oC}VgW)#}O+=J~bya28n0Q=W+Vl4;%OZx_^#R&3{&llyq'
            'USP^YW>c^^hA1s(#kd@#|3ie*s1N_=fB!%DDY2#fRGM8@<p@1jVN-'
            ')u`nK5p>)!4k&+b7FZ@$qO7|dxsL*7yC0gcAMA}uyz3r&vwa*SVF2}K$HYNQ;ZpK=b(-'
            '#4|?m=FwO8#0k^NNLcFHcs<1&Hw+oDuJoOxe~FGWL;k{kx{X$0{Mi7?H%g%$+3^}O&J_V$<BWV$=d;rIJ6d>+)Ma'
            'tmdT7h<$_=!Jbi?FlJ@kuy2Q{dF{;K(A*qSc$;QJ?C<esRLy4yHRYYt8IxD_r%JYU7(G@-'
            '}8<H1{F^ry3Lh!&vcWdYn?yEheVhqH8!y_YO-'
            '%!g*fm`AxL?0(l2;U6_B=HY81#!`AJNGpqg1m!PXWNx!b57XOzQ@=;)g8w%aF3QRrEh)506H;Y)Ys8KJ>^y-'
            'IyoD`&C6em%P88wJ6y7Jo=4jBQ!HAvY`=BeRU`cWQo|2o8`@Z^?i|WE^h1y6=@IQTiwgL>s%N-'
            'K5<BT}6CeAs9Iw}ih5Q~7PcQl_Z(kYMk7^2oE~p8&gqj$h!1h><u_fU27-'
            'M4ue(;?T2ffU;h*N^DYH9&~%iZ8922&yekb7(;*gbmQfYdFgt@B2F)cI_U)`2axoDDlXJEzha$j;)tg|9aj;~>6f'
            'XmgO5yr^Ad4qM1HHiYlm`>LrrZklNF5wQQ6N4PWW-'
            '>d%ZG)1)Y_6d?|ff+pgT{`(*_pRL4$~npQNv4Fx_^P!pTBIze)@Yj@nBI1Hu7c0w;UY>Xz$|Ktd^Y_<#0<JV8hY9'
            'Cg(3D)Cp?nUsLo=ggRh94HG;92g-0)B^DDX#o>oiq6UJLL1ahOXWlg-g3#%bPXfK-'
            'h?H&IWHb9B<eMUf9xol;0kk9i=tZQTX$FQMUj*NFs2{tfYQ8|LAADH#QpT0ei40|^C)4|)r-'
            'G4vJnAaa_(ZE_$Oy+Rs!S&`qaNfMie|~oKOaAKk^x3PI`Qh_thbNTK|ArseDTo-'
            'T+UIPy$nh!&IR;^FX*(&VM9hM}puR5lOM!{)F^gz$xR&2((D3gfj*~y6q%rNaEp8cFNAMR~LGTw+Uc`YE|5**`{c'
            'P`vHr!`RA;`_C{)zkb>m&^4uUn2MdM=?KrXZUIms4Z<yG`Ur_?E=aCHS)qDoi7Gv7($cCcp;94`Sv_b-'
            '|Ct>e}rfKFhPg_P6S49lv?@;_%I%tt<BY@cX0Ztv767Ux6%+v;zyPvcJvt!pJr-kVPYi0EhDmQ$qHJwA(pXF0dZt'
            'p(tnI1W{{71n67QurV}B!rmHVoXH{<OCX84?tMf5)S8rpRV(~Z;!h;9a&vY;sV)|n^dN6G(`ogA27zvD9y_l;5N)'
            'Qv<R9z$;sO{J{3nxR`X{_)Yxt*rmf^u7I!)X}j9W1tR88f{LLGT?<fx{yaa9!yN~w6Gdku~8JZRk7u}rjaT&4?(e'
            'LrMIjS0^u=aS*Zf!I8FrRQ_njqdh#KiNfhe9`I5d&}Kjk-'
            'kHW)UTDdTZ>UpJ;+<MVeim^KnPNFgj+b67LK)5%FdAXatX^TgaJrg5xzEgGX|*lxh`hK7!eOEY{=x^SWT-jlS(mG'
            'lVH`1guE!=r&)PXaH95tQdnqX9j#2?y*Q1dgeAt>h6cG1fR>Qbquvl39KMr^;TFwr|K|6{LTh6s6p|mmLn4yJ+-'
            'eXfzTVq2QDV<h!m=1a7$J{r;MqY9J#083{BLW;7hW#`UGTpt(ouL_2y>Qd%%rNTaa5m65|yLW9U^Xenq6H8!4iQR'
            'R_+S57;^1J($pKwYqVTRgMd-l1(lz&Yd~8Y@SZ?`3Pqu1_{DDnVky$B!=7l4p)?#wK-Bl3qJ{&wgpeb4hzQ(6=kC'
            'o6a;3R?Lucxc9}7ZCLo9BHO*OwrPSN$G(sl7T!4#^_rJ1K-'
            'c7lo!T`iKInFB*5{bJ$_W`x=&A_9%fSICv1Q$@WvT~!wsSh{DF2$BU75s{_B8LO%0)vQ>}u9+yHqVx43tC=|&;Q4'
            'iORm|SuQZcRIjG{he-ui$(S<CB;gK8tGJepzhFK|7L+}p-'
            'I^3^?lURFEn$`6}LC#@Une0B0a&iDtaRlh6%UUw5M?Q6aL+P$QE=Wxwoy6<UFZy)Ad2VU#m`>}^n`&rk^d{(|MXU'
            '(>%ZZq9g3d20dQN-'
            'R1tA=UOpm26MA^B#h+4XuE%kp)#p2@&&Ti0<1bA*~_NM#vd{8Jo0wUr^hSwdSS?ca<iPp;EkwqXjia(&VpBm!oXH'
            ';*deM+rdPk-Mx_M9Z12u@ax*f4&j#p|^zKOte|@gbDs^M}niP$k*TO1wcc2e#V#8Yyxi!;#9|RVEf0SdFnZrYgc='
            '7*sKF8Ur72_D6K21-'
            'Oh{EeZB@tLrm0>@@xVXMQSJL#K;&+Qg34S#5l>AeN&3@C8mh4ME$t)^0Ihe5tehB6q@bJ#u#l3x8@y34*>)g>}4r'
            'uT{8toZ#payLvckVmiZIf>CoFJyd30Tj0%=!l9U)W2^c2-'
            'y5~gb4s4<~Ow0y;h7)skp9V&cCP*M<OJZ0KY!n)p6FK<^T4`Q%dINUMSqgS1l+4?B+?5qM-XS{WmYjorR|nBK@U@'
            'MkNua#ANR5&klPdjgb(@B}m={v6C=$MH(wloW(uE?djf8^+11_W*(fbZ;xGS=KcILc;C)eEgQ>=eRNi8W4xVAMS_'
            '1LwnQ<W}kOWeEd)(OaG>{9C4;~JZm*cZDJkRc@S1pCR2F%x2mVDwe7COgFo6|9Sc!Z7pbVv<oSkYXGevoyD8VVYv'
            '=qf(rULc>soQ~l9Kl>>+L?S%QJ1BZsXb{Z)$6DJjuqIF7f62}izueW<=6k9F_p*I%iQC&wlolu^euVkymKl8FhiS'
            'v+FnQ3~%fX1BYw4z)85$>aUwA3hBzX}i`-^h<xIHd-jt;%9@E!{$$Ogzzrd}<g<fz|Lu=(iBxMdc$`AyY|pEg;N6'
            'nwN0L&UQL@xaXpuV+0o-'
            '#e134v#)y2MyUX+sp(TNcZvUYMxLqYbE;vQe5Zi=_9lEOZ_fg+tDt5P5yQ?oVvyU8O#k}y-'
            '|qflZ~u(lC#5d~JvWM-;@Sd+cZ*Jik=_^MiOd&0%>h}qtyjjEjj=NGvAMPVHS8iDZd&|-%Ad;409dL-rLxFI$rD|'
            '=m@S>iGRKP)I2eR57`!X54`#*ue1btAfGqHC@&5vG#@LbfsHGM~OG(ybjMA^zq!c<Hl!}#0o}NbK<7E|PTR)j`rC'
            'j^0)4+?AxFgFXTv|9Z<#TdT;=KoALh&eKb!I?};IzyHuNdQsI!ge1HRVJguAY;(1;W;<-'
            'du3W1n&}je5_2%Ips=?szjF#PIpUI#WVqY4*o?H^Jyy1oo;(N5qZMYU&V}q5=)b}@qNyeAD7+dcL!<$AXFY27@9K'
            '@e<NB0tz#7Jj5m#?>aKp&%IJlFkUG=O&W3)~W|5SR!W_<duY)45EOqL8#|<UCwiS3)qTtqv&4muyW(veE1joqi#H'
            '9)%qJ;+xq2;ir>=XB8ism+2Y7|3?5y!FkBJ8CTuDFaWe*60_+g*ZRD*+!2!_Tu7r=hKK=nUm-'
            'RM0R6&0_f*+sk?ge##)AxA-oK&=#>}OnJ)6a;$dKnXd8U!Fkt}2R)&wW)gB?(keq?6lrk46cvadt5AlkYHj8((M8'
            'KU6LzXY@o#Z=Oe5<fpVWNP^#Wd5jCSQXWtk*b1CP_>!h)%kNYZS`YY{C)sH+sCm8c5UYE;L$HaV2n?miQ2D&sD41'
            'yG*bwX7)pg?iEz2PvTXD5=p;{i+h#a&&?1YGS0X2cV92VluMvVi}K<5t1gJIz^Ci6p2|}t^^Cp@Nex!$sCL~YeZo'
            'tv>Tf0R^{{kB6&lltN~EPqNxzluV0jl&3y?`BSweeW1NskaV$!{et}YOg&B{BTxbvv1|bG?uEZsh6j?1P8^i{a=)'
            'hSXeITRMvw3kL)Xlk!DKR*m9V^~Z?N6p`Cef8^t&`W4$qO}G@~*Cbv6a<;gDez^oUr2;R%<6%V3Zv&m&lqa#j8#S'
            'R4~id!eF}#?cmfrCr-'
            'PxolA|3%6B3nn*z~4>55!OzAabehIaR1m_Jv@x2z+9Fdj0j1ioz+lsCk|w@^gBi(a0@@r2bSB2l<B9+Bk-bJVUxV'
            'nXS{T$68hBrxB&7-'
            '28?F9=~Njv0_u`yx_$NV=#vWy2XPl$lUmFH(_mvKBEIye6UsmZFsnQ&^(aa4{yE6<hQXUL&Q0HTBF?m|0+rMCi=a'
            'N9a8Tl`b8)+m6GnxZEla1xlJYCZ8ChhqN*b&+oOnC!UXT<`k!bhvd10VMAVEF&ib1;n$UV&dNC(`>3u0zM%N>VzQ'
            'NLvVoIhB*O}k@NJGy02wDu1Zz1m!)bMB_@lN~O6WSvEzYz1OgqoD^K4trx91s$vi>>}kNJ8>YOs8fe7*aGADN0Xm'
            'wgz|Hds8@F!ErnIKl?a<0_6pAO>7TF&?Hvt*4~CkR(SSS;hW7oSKAL0($A0y{rS+@&C(oATnzEk<ySFxb4P&!ih-'
            'HwIu*lYUrc{)E>z$6%wS0Rek!!iu#HLcg3;QTIpjBg$TurG!h2MGBz_zktZ0u0(ij%)0@SH#YwNOMaVG2b8nO5P|'
            'Gu-psvYVs>PwsS0?e0*=1d!DP^`9?vPSBc!7HDx+DLjyevq*uEJLl80D0E=#E-'
            'WxQE)vqt}+kg>wk)^wZZwbT!6q+Usv)wn}C!L@fGEAVGv1S1AvK^V>M}uMItENm!9rh!tYk&*_+Z2XnqeWO8c!&P'
            'HPa5Sg5&TD-5xkEk;8u&@c?GZ@hYn>iITu+ytHHVh2Qw3TC`Gtb1(aWFG12Kb+I3WP(`$3AKWgv4M|Bs+V-'
            'T^)4&^b#?bBoV(DLQGd@M8Sj}W6)tz#ZI@5mMrQA@8&D<mXI>mr>c0R9tll(bQuCa_VjSthK%>wzDhyi8Q3F$>0D'
            'X#Dekqhn2OF>u4cV7r8d-yYV937VstaoX0ERT+Qq-wbK)Eh4&-qs;#@;^anb)E5q9-'
            'hvI=QccLE@Y!sxUZY?hRF&$eUprsa*yKCM@OAiZDEy+4L>j{7*)l#>}Kb=JSEXM{i(S!@ph2s*QWy|))I-'
            '~WTVvpZ||0ZG1#GW$$8iBE55@{e^WkEO}!bS&@VT;9jQ{NtU>!!*WrHuu}mqI2ub>2f;P-'
            'NODo_@9S+A;(w4QQVu?b`*Di_H{izy~=i+fE3}c&Dv=cq>E~?E1X#AexDbsQS#GbR=q2^=o(OD41}l_r5h+?dXx_'
            '`K+$3~z8ta^4d64Yub7oXn}Wz2MWhhjt*gbz<3DnkTQYCNQCc;$%vN_ymSiFh4)uMp>X$M}&D)wYN$o*WS@|LBwi'
            'I`SuDsyYZfT^J-'
            '2@>b?HDob92EPuXfOdZhOiIk@I=_K{zUNwt`KI&7m(&gEwdH6L9i+BR{7}QMX}x5<>*<sw_2YZK=6VZA*0=bXRZe'
            'F=}z~71w9L_{pA`JTi3X%Yx&$XJ#I@hw~04zG^1MV$uPHJtcnUG8H)@9gIa_n4x?+hj$IW`Y^Vk$n<O(?@l%e*8I'
            'W%=CJ{IJu0DW{0o&M9TSB+^!zT9aEGil^(rbr(Si3kxhS7FbC`16u%ma>((iVeZvXjvPe!sT|vV`$;4<oR4-'
            'actO#@M4(T}+Z$UBBBbIh?4VjIkI<y{^uy8RpZTN>>HA2JTSA`<`!rUSZ*9Ot4N?39&6V`MP+x2HB|9k)$n-'
            'YrB9UO+{?NYV)(7EMll53!{z~l46<+7iuLW?a@M_s|*$rBWIzBx0d%?XYZ>_`3NP*r&fft?k6N^#&2kgQsXZAi}r'
            'ICeEGw@o@#>!-'
            '|R&Oxp!a^jL_2KN`>&M)wmD#cESX>X;sO@$#Dx!(|7xh^i``kdQtgSVxH|pNUlHxsoLGbVgL80!@iY}_X-'
            '+F17Nznoh7K3Ha+Ss7kQdlyU3?bkcQZYmkp5*{Z7vENJVo;GZpferxKM8ShuBcp$q?5@zUqzm<{J#dn2)YwC*0Nb'
            'BC1}5jtBgL)a%<0J*aTK6V;`(j)SS(H#YU5JNgyPNQDw4cd5S<CxBv-'
            'LNAMmxcmJSK~621JFrfJFYJlKsK4tkvC#mt(x^NjkL>kvdGDzT3|sRcA4V|w5?{#*KCdX*oDv5z(`?3Spo-HByB9'
            '`|6)BA_Sa5a81_P|j{b@pjQvQy`~2NbsWeCl2<RH3>K>(;nbEqvw<sx%{Z+Yc`~&?2<o_<zfOwYU8OV#t>ovMbP('
            '`zs1n9%fx}F=pxMa6}x2UfGKQ5fp6CS9MLv#<0kS9lX;5;7~ip$wF=p*M?!w}<FePUQt<YwQ-'
            '{ljAd1~fEQsg;E#CPzc_m<;GbJ#&hEcN}e?8ty<gFl98gH8YobYr2!IGn@>Q*Uxbpdtt`R2j(9zy=ZQ>wzHX-e_{'
            'JrMis<{k%0uz)%eS97FmzoD7p;0837&Z!7Jb!I$GTVtK2@riwC50@bH^p6a4RbvmU{Fuz>41pr7((J)1er;htj2X'
            'rg1B94+*-'
            'E+CcSqoz8gcI*1QfmHz&oK(fEzG&i>Xy7PTys7{?n_H!Jnc1;k_UcEu|5Z0w(8Z!|fEF~mxAN#DwYpe4?on0K4(>'
            '{GW%Z<(CHz(OPu-'
            '{24Rut&JGik=;P#Plg0O!Ou!mpWNJly4!HxXatyk}p=$&8|<pwkal(O33Os%8y71^T7)b@rO_f`p2-'
            '23tcf{|%~r!lf3sKnG!J*!x{WT3eDCo($)R=>UN>55vm8J=L5x{*AJe%c3}IGkSSE_+pIlRUMPL_E=~dDOxn<_;O'
            '<ts~(HGOrdAw=yu6zc3p`kF#hKaL1;-$8(4)#Y{_1ZelS^Tbz^e)=Ak--xPQFzB~>5%uH)Jaem7JxvxL9fsrBAp3'
            'r+M^I|Y1s46i=k+<}(mL%W$kR&RIO7+{=YvjgSl0o%SAO`h>94zjs37toNTRou~)iEhpi8e)?dKh3a?C5!=X>7ZQ'
            'QrM+>6-'
            '19{HrVZtzY_(dckZtX@%pNy?}{vN%$A@I5yGG)K7Ov~h&m98TSZWbf6Ux+I{0zmM%o2gCZ1*_yQHm&YCqv+=&ez='
            'lH*2i3G=OyD`GIUSx<M9;H*<6M<6bVDZ?&&5vltw58t_vIHK1i^8<V%=c0ykqsR@fLXO3#-'
            '=);7ZYXuNeALrS1O&817{{WF<48D71yo7t`MXuXoh^ikcG_fh4^fbaap6<a<q%Iywha_KTn04T@9T)jJ^EUJ47P!'
            'kEjYKyN{G>7@hw5emubqGTtr`;$R!Ol9o+Q5HhFcwG+2%=0qMT{5}l*7w4K*7*DFYFSojKKhTBXMV`JE0jCYI1&4'
            '6&$-'
            '}RJF$EN7f)AnRl3rphyU>L^@#nVagzI;Nn26Rp*8;ZLwfZ)waVjD%m#s+#R!4JR}2#Wng8Yd9qmm4fYzP{W~j^V#'
            ';WfYbcY)Swz`i)O#b%A*QucN)VuXUFmXb3>r>8Y@JT+h$z@9PiH=P5wwiNNdE&#OgwG^s$6czwKSE<Z-'
            'UV(cFSjP+lm^1~A7<fg&Mi;)N(3F%7=5DDFi@g+FfRZ*E;9y}cF1#}D%?HFS!;Cv2ClV$D2UCVWuT9?wiUXKnn3='
            'U<x(cxkK1P1%5DPPi1PlTxClLwj@5miw<u|9n?cH1Q!jhi;uI4)bwh4t+*YG1XKXKc3{BSz%s^#|2X;z(H4#lZXg'
            'YA(_vA)|ozW6wQL6KYpQldB9;L7kY{T97X@T~@yy&G@p!ShfB=Y!#fEF^zUK3n#}%hYtWb01bYOi_l)bNwuOl<7-'
            '_)J=l&OOZb3>g8rkcRT<p_6OA`O=jYbZP2LxaaSW`Yy(H(<1Jf%68zXW}atzlA{@khTv|2la0ByLrw0NoU`>98<7'
            'O+K0R6*l_jtbf;V&YXr#;Dz%13}aHI97a|wK|8FwI=jZ=68cBtl6@s9Q32WZT!8p%%0=9dNQBvAU=)eHQZh-'
            '1RSAxAE)njc(zWE?#H+N5$NEeMBAy~9o!<caSIi{VdTDxh9B+K?8Vlt<R=DE(P*L2Z+kcb>V5SJp__9t3k+huRnY'
            '-#qeApy3G|mlnAqPYFo6Abfb8Orp`M9AclBGar#U-N|F-'
            'FkM<O_sczyyyn6Fc?E58^L1?1}@Mv6Z_@sX4$0a$Mj<GxCPG3ZG`E?D$bPZYG()}T-'
            't%extaywuKjv<J0N65j?SOTK=DCCE?tdS_!$+vDmOfYic2p&3X>_@Sh)@y$leEV`j-'
            'X(74)ylhvhT6DB;%?$}UrK+?{ED~5)xhYmaLniZysbB^-'
            '(w#3erR{OCgno3fHL*Y+w#e?hXVsu;cd!+z{mPM00_(C5vPQ&Y#eME5PJ8iA`tK^h9z|uY>qR0oD~pVdR;M$=3aq'
            '*NJ8xeN(qh&XM>VnJiBD3@MGc5V=DewAz%`%(1s9_y>x!m}VJ7i6?$SGs%-o{iSyzoQ-'
            'lUHKKaTU1hv~*WOH6CuhO@pf-mz_m5Ra`x=$CDDjNn~F?)yXt;atm?3P5+R@MGRuW66E*uCvR)XM?KwtXnzhOVC<'
            '%9F{JXRVZ-'
            '^DplyFQI0dp*o}b!j>#>8nL6+mW`b3k5VU*QRwjaOEsDX_JBejbCmb@;Z4IMOY0uNvw?RD6aS&AO^$lnAYd4uR!|'
            '*g;yaObawz+7!lCyvpMu%xnE_zD~-'
            '^UopJ57Hb7V<V@O(SRN>y*>m$3v~UYM$^XT)M5L>a#>VORNV<0&BXT{C;n!Vr}-5uko+?9sKLz-Ypdx^#(UiY?wT'
            't;1pxq!I*9b8F2}rjJqb1sf-'
            'o)d6>xEo9KeaGm)UM2(*K*_B#?E@F1BN9|j!@8zx40L$xmF`}E&3e}7E9)U8GK>|31#ZORsB=zU{s10!8TA>?i!7'
            ';ZQU=CAHf;L&rX_i(9?gbkgu2<wy`ZB+MjxpI7-'
            ';}G1hauiW9lxd%s#ej3kr#}JAC%DZ4^s!9P<0;8J#Y2kibECAU6M?i3$GDdLwsi{4hVlULybmJ23PHoUcB|}?Zne'
            '{-'
            'l5Kt0NuimII!uP$8Y~wD;nv{D?IG8OzmK;7Y;6I2&|+LF*aU5pSuixV(_pr3jA|_Lg7C^hO*YN&qMo!wya#tM(ml'
            'mL5&O3Ych_qWulNa7VIQQ+#YNiLMM{o?M(U?b`#2|H&%&cPGMpIHkQfJ9G+Tu!v^Y{-'
            'Ymy4u6d@oi*XWfQDQVi%Rj9qAoTQ~UYp~V<&R1peZl`l-)Yk-'
            'o8i8gX{(h%@Q!eAb1rjOSd=vCvY7rD{tA5s=VWeARXcHg0w?QtkazW%4tM(Pg3Ly)ULVXK?p_lNmEuY?pZ|~L7I#'
            'lGqX_JWWX|Mh*87C|s^|ZTP*4ZK~7WEsW72~X<J;3Y1<`D!++D<1F@Q_TN$`}HRI@-nJwxbo23CY<o*N-'
            'FhYNr@47y7P5lfznbv7acmPooJ`wC5<d%vy7&klzdoF#CeF2r8Nce-'
            'WP5eI3=4(yMjICno6McNg7D*gue;Z(vj|X64Cc-EuMahRRbhqUP#J<F?@6dokNBlwRt#0Q)z~b{4<=Dn_{~=|^eD'
            'jIvqildEl_8|`ag+G59d(DF<JN1?ng;wEBW>RU{bfl72DQ|8f%NIRoGWx=j835slGFFBC2&0$(RU|Rf0$j4)wm>Z'
            '2z!a=Z%1QOUDgmG3uwd3O4YScKf!(K37Nj+9rGJT-'
            '>!L*wNM&h?WEG`$T`=i!}UK*Mq>(A3#K*9IwF((^*hU19QItPfqRTgu2M;7o-oS9MOIF-'
            '&ee;+<fBDTR&*`aY=l;Us45cLgK46<_uo7m0RrOR0{E-'
            'wK=%T*wLG1z5Y*R#`V*{5kiRliWh(RV%T?nSgPlCi9&&gBITQlmkWAz%4`v{Z}hb^uep3r<?dXx({)s>gshSI()i'
            'zD$K-mORknQhtPHcQCpACDxu^u~9Cpo$$nLRd=>o-BA#Y387gqy<>-'
            'M>LYDby~$ie&1l=HOz)YUyHlfVo79Zm)~vo;&_*k@52sK?kL66QlYmpZk-XDTFidQ`x<wf1#qaO*xeH;B^49CnB3'
            '$eZEz?T;#9X#oBz7^qhLc^-wfNg$u*-g@D&KT)x3>1*(x>mUi5GGsynz00YIhb6IB9l5fpn^_k;-'
            '1^Gw+JS*A?W@@qwV-'
            '(k)bhwfs+3HF$gGUwX0m+%)n!@s9(Qr^_ndqBEu9(<IWcMk3q_9gb&IcqCr~Y;<NM^&%g^@<TD^GT@XLYPTUxI$T'
            '?tifgRSi)#{TW$sg6mJZc}zuD!uccj^>xZ=I+8%smC2RYQ4%4w(knPGATeznOVE4aemeJOfxwblGl%|)CXE<>^d^'
            'aBVa<}N}eDQk=o5KQSbHwedLS`*6c3adkM-)`af90-'
            '_6W0F0y0<afHK6rIP>E?!3^0{I1GhSo*w_Au=sxNke&dlntjKoBkLsd0od<>f>y_DNA7hT^y*GRIhutNfcWmAb%n'
            'j*up<Y&jZfj^EI-wi&Pl%~XDI++WMp+;0urx8Y{)L|B}rNSgNdvZ^5u5IO|<FmMZ`_E*dJzXgfFsO>s!bQN*#jHN'
            'Z(lqLO0|NT(SE(O)E(YljK)GPq(Lq>&tO8ecSCtt(;Em0+lHyKbUl!5CYq7Z4vKsEzbQOOW$>tPcJ>JZhB7GxXw;'
            '2^4WcswLh}rSWAMnY>bkXQTH@n6f!sV(G2@XGkwED5TmOswk2)HVWcpe0)X&{yt$SCwu*$4T`7ZWOM?1yJjVr@TI'
            '_zEPBlGr617p)xr?a!Ws#n3p6J}GKcN)Is{5@~!N2BMsx{EUk50j6%r8_ae2?Lo4)rP17?Z@<&zeLu#Et7}$%0Lt'
            '35DZMy-'
            'D4JN0sBKF*b*<2TQ%*Mx6{f~gsHD3{Xezq?sQ5(vwphgNwgQg^ofumkQ7nUi+HlB4XMme~S+AdBHeK;X33AXUKSG'
            'G<|L#DcYA}h4#a4^bm$^X~a;o>;^s!Cbth`l5GwKL0IK%kF&c5Rf2V0b;*OCE1tC;~eJ%Ia-'
            'q2i*zIA1@ja_HwGrunqs5C9Q$9nLIqmm-8_-'
            'RWmoH?VB2GzgS<UWi)6?|~3cuZeC0oz}$oPDvHeBx|*FFM9Z5_q@Bt&@!j-'
            '=PXhC_ozM_&%vBiS)+0>)<%(zqL=PII|{tp7<XX*X;yOA2#rZOJnXisZ<%UFr?(1Z_8zlvv09VYms}5HXE#?Aq8G'
            'y`NwdQ`^bVXJ&Xv^=g3|$VXKcvYw2H$1BKbFz?orC55<d53AzPz{R8mk8D`u{!7RRg}Q&~`v&>ya%7!0qlnRMn7|'
            '7|c`{0x+$T6>PS+Ci-Tcv?-JL-'
            '2C>8ll#vF2Q8Kj3&T#N&kY>sMD8bgDeneYDH)7xcVGh{*k<w6r9@GF7vQW&MO$=(4I^m1Pe0>I|Y%b;*q566O1z~'
            'fO)o6iL8`G=0;w4FFqN&;)D$VV#;^@*X^T36bNV4#=(sS-fik-;^zdLda>ed6i>f?9Dy<;(4-'
            'MyPym`=H^5=yUpk+<`5JwXMPHI4!H#&Ma!?)PO!<Q-'
            'VUm;=<gny6s9z+M&fw%%@Q!cJ2dnh$e;n@qd$If1z1=^K^4+t0h!S~9VI}s;GMS<<g?6d6X)I@n!vcbQNr>^~t-'
            '%W@4ccfqnWhd@DA5&etNBcDLE*K)Y{QuN{Qfb{gaxpnQS-'
            'M4im}@;SQh06croO~70;0hTpU14gELa{q=Lue%Nk4n6k1*<PDO`9%CgAJ9bk(B2ql^(Wt=3svS`3yB~^U1#k{Ovp'
            'wofvsjnpQ^I{tT1TEBXIaUTU3I14I#SrkcNZ>O%?kM*B^acO8&2M;Uvq*!O42z`%l>q|ct8!kyFLR*R>uV3*&foi'
            '{^d2gDfI}r%eM47?F(Y6xnf}!!8Y|aQJ4%(gN%d$IeRn2ygY%r9Q9Ok|EEdsC`Dn2QZvWMsy0>aoyb;YThC4g?o1'
            '^1bZ%*^)M=yUk{V_j2JUu;n^O7$WKA$K(bGP(Aer>)QyuG)3_NT$0_J5t+!~Y)rI{7O5(|_Ur-pk;_+w$m)n&97m'
            '5}Eo|DfQ&L`RitH@BAD1@2}6tzoutjW$@eomF{HjN={$pKfS=nD{)Nw$%D~e`3L4U(z)~ZSbq4uY#={;Ek10-'
            '2l;z7Ue$}hr^foWki+cCahB?fT1z#<0I+XHzt<lc`%AT;zkk2Cr$(+8<ICX3vT;9unSN<}xfM6SeVE8rlhY=sE=9'
            'v3#`_7Cjrf_vjRE&bC8SADy#OI-ogkK$*rC8j2&nJ{+!zi_2C2jtm2LO%VjVwuYUJ?aY8E0Anfi^yw@m2_Qa*d6%'
            'A3^w49Flp({R9ejET1mV&`bOna!xlK+YjAAa@L!$To|LW7eR>=welGmV<{uw+LqC{n-'
            'g4Daa3pvIKn5C2E>$#szzAvOdmS!-FhKz7hj?bxGOKFvZ-'
            '6<$wnX8m;I?^Y1>@P%LgP^Cj~t_>_zs!%{nQ3NnvxIS9C8G8d@ZxICbgD-'
            '%^LCAr~Q)dzYNFb0p;<}!RY7Aj%8alM%_%Xp3qK4C9_7Lar^9~s;ovsSd=9qR~OaD2st#H>cu0ryY2ZGkd8)hNQ9'
            'ij(Dg&so*;;PvN~c=vuNRJmh#KxR4JI^dbH1k6G5<ml<)PtQ*!t{)%1Iec*hw=92h^!V9}!{_<&^TWqSCjni{Q(6'
            'd74rO;0go7$1u28#&+&+~`9IunZlgH1V!7=dyt%p;C&<u{U7CfX^TVFf*rpDXD2EFEcsO_~I;+F@^+Vno;6sVuxw'
            'HPlE<IOh>VP}E9GV2m#9!ADJpql`ci%ZOy=^nMh&z^K$APB=4(Hj3HaCPYHP?1N~+|qdKL1f}b;kyI(PyDt&y0M4'
            '6oeEJ3Jw8Y5REu?`j3j(C1pd!xC7A6!r23Na_SkMJHV5b-nQFK!O_?*(pX-'
            '~0{TCNb6{|@#rp$sISFbHJIE0WimA_@P854&7<uAYNKS<{DVe)+cA^h)O{-'
            'RNm=AP_3<03n9yQ78b)tZZ}i858h=e!+0I)ncaQU|5{l{w-wuMQgyvEN>wtSNEp{2-+VDZ%@I;7#+B2Uoh!-'
            '}l|`sh{vpjMgzLdwt6H0!I{kR09l?2bt9z+L6fWCd8M6@TGTu6`56ZmV8GKPUr9zo1DopOtj(OrG0Q*m#c9AW#+|'
            'li8!+=u5=2J5X!K<*w^QX*~H=7A)L^GhVZ%gb_9lgS!}o$ykIh0T^0>#kLZUK-'
            'Kd+i&DBA!HR$d`!tcJ3fMzEaz&O-tX<%k@-)_QX4%E0tsRM%(vbx-Em-'
            '=1++}h)^s3;^8Jrpz$+j*DRN%GmWUvu0!U#n_mS5h=i4I2%U0VVku($X>p2RhW^k7O)==x!2c$9V@LCqi~6IB5F&'
            '!CBUQOAY-ZFG70H+I~v%7CLR|b0}RYyH)E`44-'
            'XuKZFlwrZ`|xdu}PNZBxxRGuEQJccmFfs@;BXNs2Ef$#Qc(tH#NR8u0~me}Y6`vtsOdT>}o`mZac9@023{f?%{G1'
            '_v5x2lNzRdn~6R<ZG-'
            '#f#Q>aj4D(~o{HS<&>TE;I%eStZklyabn=>CU2NuL=EU_5GQilBR&}_TJO$ZzT`nd+0VA3Yvp(i_Q_a&!dwG?Euh'
            'bf{Pf}9aG{pN|#N@&rW%?Dx{j_aS);}42peIDgQ^WO97ie`zX!}#3BxONm4Ga+*Xv(#;MH?eqcS<ysZ=vA?s^=p='
            'P$3?8nG4n36x!5Z8&aSOPKGD61ZFXlJ$&xSSMGG2gWvI_ky;4UfTGDp$PxD$U|J8soSd2=VItA0hWPuaAA;<IdJT'
            'K2BDPUOSSpD2xntUZm`)<OZ^*|AMeH#=RfW?aV|J9*AdrTOWC+;?r!E_DJ$$v*P`np;ta5GDjqgeuh3{}n;~o1kq'
            'mQ0wXlhW6wi+)FI&XzByq3<~VPc1=mAO>Nb*qVOXvnGEalDzm2f&{>qE*_4I|~o2a5uhCDc;*?=rqo{wc?^b)f_S'
            '$3G8u(E|LU)ndR$xc0iiq2YZJ5!Fgl+@XgS!+DumgsCdp(R`6Z{w=$42so;wCrGTJWlOZn>emcRdOt6-'
            '>bb*fX>zUyjj(@tY;oLR3x<o6KG@47Qi!5y-uBh0slBF#jju2?&8eLe6Fe9#6mY-kCoD^D6QH-'
            'M*8|o&@^dD9+p(Uc+YC5jGnQ`Yj;T}owR0g?{0Pw|g{5%TPYYX|L0Y5hIix)aNKhu3y)q<1I*l`0I+Q?+M8s0EcR'
            'ZvdxwqsFe!<JwTD_N-toLKorv1IAj&0Q2~%fMZI_pq^4bE1=vVR%J!<2@Vl0(%RXe!84y5pYJZ7(>(c=ZFkXVG32'
            'PXp+48`30V9vzc?XBI!gXgbKqDjSfZSN+ZAWO}BYQZ=o1>rM?}DU`NF}TDlQ|fpX;Fdp;EZot~;a=;2XsfJRDtLZ'
            'NmvR%Ql7D93U?7Q*sB(YQBApB}wH4$&F#ev+2+37lH9Nb!$JiRn2g;EcHYX7ph`ON~4%gY-'
            'p>V!>t}9_^}LQ8hU9=^E9Tzs~f^68;{+3L`A40Uo`B<5sMMk^FdGtlo)>5DQb_CS*LYd&AO<?%Dv(>rwF=sJ?M}W'
            '}ZOD18JY-4vOQw$h1kB?7AWMB%eqSJWZD%cU_|uMFyl_jq3Mvz)gH}MZ60yD?%S^`*S3BN3a+K{>QHM-'
            'u`t8;)1jRRf`7QjFTI6!nfu{WzB)i>k%Vu$i6Dr1s81Kk8b&P?@UF+dmFQtZvU0OtbOMef;ag|O;P2ZpxPbC0)}`'
            'HePDktfmj^*k=o1y@O0z)J&N3>a}K%8v^(?)&luxV8!sUUEiRo_{%nE1aVoht5Jg~4JaW{a_y#yUtu8RDw_-VjV+'
            '(mhvR}(}@}Kp&CDR#xUV-~<-'
            '2>(2!vxp$isi4PL(%FL{i$4o3?~##fU1d~!<+dLOD>MTlg^S*ayyisLRwMvY+`Cx&vtqy#1VMsABN+yZm;3MzgPl'
            'MkWHYYIT$!evaqnA$Cw__bL+qBA?_+No<LS}P<QIhf?0!!RG`3_c#RA+IT)BEqFlg(zCtY(<D_!16I(XuLpF2^f~'
            'YoxcnZvK=(F?4;Ol82&d|mq%86njR$IWL%R8XEv5!d_fd=06@iMa!>TG~ezFYy~tEWtEtoa<<JV=9+XjY|c%ePIl'
            '`S`ZADU3b9jij&=2$<}Gh&Aoa?Wcv7GDuorTa`sO&_eIgFfn|G0Wd{FKI(BkI*Mw+IwS0Q8QQ3GD*|!m=DrW?E7I'
            '0j5G$XJ4sbQ{oFql^#KJ(%KLy1D4bN~RgztfdwAaXo{DJ=|#(oG=Q#8mTlWJVp9Vl6RfaVB9RAjLqbz;d~aeR$wQ'
            '8Ta{XBNz=mJ*wQBf2El-'
            's?y&z)m!=R7}UACzHAiKXERNA;O6bcscK;YZs7HL_)%O)C0f0o21;B@vYtaOo;|NfrL8Vz*+KL^1!!N^r0v|RS{?'
            '95*J2|WU}GNj?%DzrIAq?>W{=eF%W-'
            '^TpPdRHx9h+B@b>#ZMh!&kY|Oka(BFRf&X6!?fw$JVoK%4WEblda>LRIm$@GFF;dDZf!^o^Ek^sPDLJWuY_p5E1W'
            '4><@xB6tB)49DGo<><r^;fyvO!<<s=0(|H;W1wV`ZI5UY5XjCl{NtX#iYJ#T+jpDfv!R#mrlvzzs1usipC6f%!&l'
            'l65tk<^Auvp_bGu0h&=MaPKFYN27lY4dS4<CAG3!%Y>*~>Lmr#xAIQ$cHX)RdaGA+c4jh;?)5Q8^Y48i?A*AbM&H'
            'Q&{M45Yr8mS0_DAG<6T56T=GO2sp~}fcXGZ(;a$IZxH8I91Je;;kYW&5;fOw4V^y3O6{<{*h_!l;Sf9}=w?l$Sbt'
            'S;vB#^ggh8*mo}#(@djTS(48M>2ZXZIyfwa{{8rj*C&FC|>CW8tSFEtP)vRY)QFy-'
            ';DixJ~qlEG*YaGY40$9L*7OHw&VGawuy(XXz2Xy+BysgkvA?BO@V!wELT{141V=H1w=$^?sz+M2|+26#|ho$7_~D'
            '-G(}Dx$oP^umYwkojwV;o#du9xuh8b(N|<C_tU$UGK||8u3BPEIImgRk&<e(*pwH)`UhFnkDAq{*2JHc{g(Y8{Ph'
            'yQyuh6<;xs}B@m{b{?rIv15r%}e=JlENHaA10R32WomUM+P}m+V)>6=X>-'
            'KdHy$D*|h$IR;sBc>K(*`k7ksbF|5;g2!SRR1wheWwE%RKx^nhp`{EjXFR1LfdAhtnqulZW>ciRYIh))C&6R?Y}{'
            'Gz2X*fKp=Sq9iYrdO#*-3hGo}|(VCCbLF&hLNiqQ5-'
            'pVq7D0wZ@Zu_0>Wnr@uX_vJ+NNe$?9jAKEfZ7>N=HJ)!3@5Z;10Wop0&NGt8$whW`@8C6<$TC+hWaaJFv=JU~EjJ'
            '<@>4*nP4dQJnK`aoAf_<$j?0s~HU0~BXG*J#)%MiPqn+@IDS4$*89J<X}!+`uR>s7J3b}ts9-!3H-'
            'u<<h%w;?$16S~{DfRQ8vL@*R_pm2i;E@)gYuSW?bR49eUnKVmepB2L`SM_8w21$UTP&W&isRYD<=CT0#2%CWM1+Y'
            'm)tqF$2SjEKq_r~>_jG#==jdIMnjdRsUI_Y#~CD{_i{2V3WnSXZ>S$_}zKyOJ=ybVvWrGKExAJrGZH8uURaVe&c7'
            '88+=P@OX&hR;-'
            '|9<DsnwAX%^My`G@a_<$=*~VOCJ~f~4sjj`LJ7=!WGv?6bH^$r;$pp6zx9PskiWc~nzb#x#JZskWwVexnmwYqVwp'
            'K3b{p|?T{NrEidY-Q_SHhZAa_DX*@_>dD;ke0Z$V0mZUJ%&6Xc`<NkBwT!6W-'
            'vDKs;vJNAfwKjKRza)|3;+xJbN<G1e0U<mbo`FD@*9otXUK$`+>F(I1V(2)-'
            'KBEgRcMu$IrXYcypaB!{4V&a^na@`G%fJI8b+H=Qd|f$2}nIqo?P9vbH0Lmvzg@gustsJV-'
            'o$xU4w$LZW!Zq)PKW%}*mvTf*##8#cH72)Ix05`@$ZrNLk-sKf=1DHX;<6sSX<W@wMTlKN4hhq-IFyx(MN@-'
            'i{e@lE1dho<Wk-'
            'n0qC1hq{YUMaz8Wb<gzW8*`OK~2hhzRW0Ys6Y&4qj3_of#~^wS<=2o|37hZ#*H>7s=t1llw<6P;hv-_wWzNPZUj%'
            'JRCg$ByKJ%QuyI9;Nk&Okr4r0Ms=Me$i`qY075*NfGdJHHzU$nGbg(XoNNWdDz=2U4dOtIu^j$eu<3v@{1z_?${4'
            '*up>S2Mk{ZOrh7$n;R|74Kp_BkE9v0yr)T}YCrlzoCN<4zQnpUf3%_6`qtJ=s#$WV-'
            '!w80kjGGk7a0ZL6yvlhZFPxB563Y-v%GmsD&F-DWhQ!H0K1x^Bn696Fkf*xd}?Q-'
            'XNsjT?kJ4hFehYI0XZIBR`#W2W~nM@6vnNQJaeZ(EMO$8{{1E+%;Gh)2$H1(}}+p!!|1LBC+o3dPqxl${GeONnb@'
            'jb4Bz+JpltQlNjCAFJ*vzgBespV9k_XCPhpn~-pqnb%=NJVZaGTsSyS4>R8W*Rl-'
            '$YgKW*D90H7GJzBLA9sqL~=r`OF+fB<Er27o*}ho7WP@2rUq-J_O+kfsDIzyzwy9zYwF{sSm9PK#bi`r6a^5chsD'
            'oIhcMhI_rZTTJ@jtPzUaxLez{F8^=lAICa5}{HJ=VkRB9`9oZX#rrY13q+8Mg&U0s&5xnkULbq(emqWVmlN5^EQW'
            'L|H@@v3E!nUT1gKU37Kw1;c|K6LD}_d>QGV1n^c<q%bAsmg47zBHEaKioUB?C*?+%HaLb$+1g=OLNjR9gRlG;Ku5'
            '+i&fQ=dA%yLG;>|vbPhZkDAPHZ+V7cO1c5hb^GlCy@5Ca4(zdL7&jxXi+pbAraNYi8-*)jBP-osQ%)18{)bo(tY9'
            'lck6xmIP0QK6(iMjG;Pa0{>H=L!EQQX~t#*X%d5Z1OX-'
            '*i6>uR48VdZ@C;?tl5y8w0)F|K=>Sh;aJrLUf>^mDR{i2C~EiV3+H;c(naod%}O0a>h!g;SKdYhHv`Ue6g9Imn))'
            'TQX8UY&=ih;3sb+L9hQ`TWP%xE5mc*#_Jdh3m`JLuIzQ{$9)YYhZ;06?{_$$Xws>U{zXV<ue%m1LL+WbEVny&UQh'
            '(IEZu&}p?08O6Y4Sf7=gsmFoU{0cn~!svetZ7i4W87fY{tb>2Hx3$H`(pC_s_pOFyA(-'
            'Piw9p;e;H6f0h~UgYA(!Ea(nUX+*i+4Zkmy<b}XN*$<H^w9~s|KJ`rlm@(rtC0{%^|E7GnmpTn3P(^d#D9RblOee'
            '~%VFB)3#5cA~cK$C9#t+85Cwunt=fmgEp2+E1hyIs8e)G*<|9wblb<Fi=s`a($8JLQvnArg_hIsldD9hTdj^bAKy'
            'oZT-lE>T#cpksct&B^Oxpe@yzirmnv+_ImeqK+mlbajBiNzY2lz9ab4m=Z!X1Bp~*pK)J%#6RE{OjnO<@!-'
            'V5ZO<@0P*+1!{0wjZqX^|@_`zK8$Y17z?586i~VE|{_pGMhh$GQUt(+d;{)}>xA(=uzP)^4Ul@}X;6;JocfMVI2l'
            'q;fgZp@U601`n)h9VH@ii5f6^0-'
            'k1K$KOitiXgUO6E826*1!kb;@A#%sh!W5`h7$MyWYTCgtJ>^|1tjS;@RzeG?Z1i6Ehfw~K_<vv3EQHn6~laMvZU^'
            'CC;@an5OnmFql^D^AZV>Ks%eYiA^`((F)gAv%9;fce1fRak1#&6x#s#=$t)M1uV#(?%JNG&g*$>92L;n_dL(`Khh'
            'kWL@dYE8Zlz{OO%xK(<`Y+HcJAb)&)QccP~Br8@)24Z$E%BCgpS$eomQ02<0-'
            'ehWJrMwlsR;ZZ$ZBwDvg;I@hen?rs2aP*o9i!Ll$H3Aj)ts`ezJ61V*H4GZ>l2_M_`mB=j~_Ob?4aM+*N+i5wLi{'
            'lO7L&|jmP}FxUNk%Ci;kTS)WLeW`3DWe?fdSzhMc<C&K8goO>uCF15s(2C5s;A-~Ebx1=Jrc$5g-'
            'V$$qVp5fhb^PY8T((^&Lrc!H|JJ&>_TM&?LEd0OqI=(5XL>0z|JoskM{Z)cu@Y?^^NdDv5Wc0iQbX#SX?%N*a)e2'
            'n<IS|DF`^fk{dR{ChL<`!D1?g*($;UFABHO6U&%3UZnH&nF!%3;oY{}<HC&B-'
            ';_4VTS(Rm4^Y`{BcU(D2AjmT2&EC{3$J8yZK1=Ch7)S)1Y`Xl^3kn0@jZ=;iWU9T^Xs}J*HdAfpk8M(kAv0Rz$Qi'
            '!a&@+ef?yY0qHx7#o3r2CRS&p6RVd4&fUs!-'
            'F%pw3*ZeTJx6SDZF8EL~pYP8be!xT+>(*x@u2VzKmb;Dq0?kW^L|mut5@e|0<X+vc`i>AOSuQ1(U-'
            'AKDs>C2M#(`|W+>ghSN$ri54M_kQpPFIWm4H6%O?;Or(3M|;qR_hZ9Q$UX-'
            ')9dp8Yxe?;%k4nb03PX0tqkd6FgE|c(^$^uS;RZIggxiqkJRy4cckhvpO%;CcTUSoBc(_&3OATf`i(d$btz)&D1O'
            'K;K!D6_Zi#KvGq~2K+!9P^<&D<NoyeWj>-'
            'vri~Q&LgPR}`vHj=8cU<KL%(WYi$Ig>De(m4;#Pm9<2N2nc#xymy1v<xguQt}`T(d|`&-'
            ';)Gk%6a#a<p*4H(h$pM!>M@^e6AH$6_zuNu5K|PsQz|WZ?;kAG3O5OYH-OY_*+C?rfPw*MgFv?*9ZFsg@&jeQB7%'
            'F*Ip%wkqy{=FOt6aFDUuo`p`l<wJ>0IbtX;XRU7JF;?U{R@W5hm+^y1tkI;pXT&KX#H3c)E@8JziBkxfET%@L0ks'
            'bx+sBcZm@6rEBnBB$%9-mB^wjH>44W;P2JL#3?5Tx{<^aQa-NL6EJit&6yM;mUdj{KZ%(LW~Y6EyNpSJYOJ(h?Zv'
            'KTaSY0>>Q!bw0rswgK+V@d&$6RCwLaDQ*CTgaxy?QAI2`SHOzI-'
            '>Ew&x%%>iTwh03Z>~1JW9`=B;q!~yj8QmD};)e7IP%;?nV_*YVC>$uYVAeh<9<Bwi_U5P2()H#Tk<(kWRJ})>orw'
            'sVr?cXM|9Xu6&8ujq|H5v#B<exDM7^5)vMQG0I`N$xn5{+(wnjbY%UX;7Os>$cRrH;RXoIQ|isp3K&EJQQ@SEu$z'
            'W&3%rdjx%iJwQ?l@+u(&T6Wcq0eiu#S_~xO5kuvKy1N_ER-APn4@*gLyc%QcLUDL(=;fekrq@l+2K?=p0|uVC^V8'
            '~mdeSjlW5gwHGgQW(i)W2Pi?teI$I-'
            'K0H=eB15Zwu=_py*Df2~E6XEYG^M(mEeW08bhNpzBBGR;HSU1eZj#)#t7Ul^yB%0O%H5?`%n><pUZZTtn&d%DDxy'
            'rgbfPcL=^rDnY$8ubz?LjN*IC=>J5i(_BrSuV{NY&s_j7+Ka4Sj%7QSBgohIqh!x3g=E@FtHe44S_76p0ke#ClQX'
            ')ktcwk?GCK3mFxYiQ3yB-QATv(xI#=b|96shc6GG|M}$EN&fQi#Zi0^?R~qui=J1z>v~r>Xc<_~MHvrL;&k)%3X^'
            'CXTeoNa_gAl8VA|HB|8;uw^7KSEyewzSgLGQ4ipzF~#aMTWDlfE#Rl3QgRz*sAw3q<o-'
            'GV(f#LoEe=_BrtPhY9TM04Z9u8`!U&n_1AN~x0X&x#F}B{I@SODnf9dWvyui?(X45D^E@f5TK`$`C#fI_Z6Q$i!W'
            'CwBA&u5q&ICTh8h?O3uf~#V*l8uWi=Kg{z;-'
            '*6bL)D#`3idS%)dW7BfBVb#yTN<%5f<e!N^*>So4??Hx|=PqWL)#X}+BZ}ODkKjOy)%cRV9udgJ;=+yr;}Zd@e!a'
            'e|v8Zx6-'
            'mHaJR&(8q^aouOR`y`6Kiu7STtQZ?87|1Aq&2&pUazr+$r=@o0y1b{q<^$DHO4m1U?hJ=5;DlV{)cAx#Em-Vz&z#'
            'ReYL9T2~31=IWgumex`GmO>Px=XH3XNvN&{Eq!N;?@gl-'
            '$|6}r`QC@LjQ%5&!bmMN!obp)GxFy;|n1F&|zo_?~VY&%X4YR40;pgk!Crm<C<(x{@Rhs&0<4>DOrppAw3|gqsFV'
            'zIN_a<PgIXs6g!y=xo%lXe%L0%IRjIUf8+W3Hllf92WeqVp^OgzugB5(Ztf}c@nYMOXf^#!0x;|+PdX)eFttk>3R'
            'PVtWM?!sSjU&b##JL^&w3e)|Ak|1CNa_)SWX+UI%b^!-'
            'Xs3k3h&m<}j1e`L{PXMTGjv0{id;r)tbx5kBbDJequ~u#EG6Nz<&UB<MloeoVH^F;<&ARYt6GA|)F)oS&sY+RCpg'
            'p;nu@f-$Y#ExGN~iNn4x5U&72CW{Y^+vi(9R*4nN)d)IVG*dP8wX-nU_CFCX6IGDi36_urnR0c|m&m1z7g_N?Hq<'
            'iDFL&WnxyCll-6m{eNrw;mEWfTEoKWqh95~gT1|B@&{=|4A1<co&YbpzDBXd{xX6c(Z9pp57+Beb-'
            'r1b+!HU9`ZW6GFn>~_XaB3kV@%8~ZDH0(GrDZ3uhCbJvENBf1+d?YWm+626@jo&jya|(W>+XU5Q4J@qRzEqcxR~U'
            '1VDfVz6L@=Ef$Z%Jt(a2M8-eBDCGyFhSi#iR$l-'
            'UxRNHvz<`$^OwLfCL{G{3>QV9(m`SR7&*_aYTEpTkB`YFsOF0>ZhNVTBUZUK(@jPLTe8VD=DKy+mGr}JEB*~fq7Q'
            '(~1!BxBxA;1QB<&z1#WN`C}E>T`6(l}fZ(j}C?y&1LT95fMu5LjqV2DY75qZWz@jF|(ouY-olKsK&tn>jL;4}n!?'
            '(b*#LnV-9tJ-k&%cc^=!BCbtr{0W^eF&gL0=6&<~twjKY`Romhq*cS@_mRD3k-^B)2(rdsv8wLuM=}P`jSLt|-'
            'm+=~J$og)1^@oanQCY}D)4WO!|7QIGT1BP+X#pIy~q_7&@j2|%*g8`zPzcgn(b#srS(>`l9u}fUf@}&zV)8=Xi}|'
            'DxjK6@@Fy{T1~P6oZrw{w8GS{N|3F0lczFSVY7MpMZ}=^^iO|CN?5zR<UCH<N6RY|~k9_v>Kev80qH;ECf^WB!A%'
            'kkSnEqU~_Z<c!UA`LFkf4$<9JQ-md9zekO|Z%(h>IB>8VL4UI(ns%CMV-'
            '!u|ST`3c(qTLh9bLV3j#0GefQvX`Ma6HgNPrx4GuK%X$xVC6!PQvb6&Tc3Lf4TG|Lq!xDPRl~N(MofytDqx6{CHm'
            '9{R`$jK`NV)MCcKet`|IxT!EYKn$7)g1PbD<jOc$f6p&MHwoy{ZXc4T&kVGSbb}8^9`(fXJ0f$wPzmSo|Df6c<=-'
            'Cfw~M{1obf3XxnTmJIi`7^Ki3z~n@_N@gh3i_kkSX0u4&$M}14IGcreV$!a6^n}ZM{N!nL-^PpEvUB4F3k+oCz-'
            'U>M!OQteB5o<R8T^f0#NIHsm3AY|XbcSOI}e*>t9I0hbY6IuHi|%z5v-'
            '=IXcQR$8zA4_1DPTtsAgR#)zv@8;4XBL?u}dCh&w^zXG6&tri+(|A!6ToG3f(zGKP^`Y|9&NAZ{3B)S@rm7;l6xZ'
            '2YvqK2)DT$xg&H4^hBcn6jExS28TOg=NT!^Jh6iU8@-'
            '5qHgORp1PI>@dC|^Jw0MUN@e5VT_?=@_gam8{;dmQQpt88Vt<CjPH<$_%O8>@X4Mso9THr}QUOZt<y}jO+=bRPJu'
            'yyB<s|^5no#Om%=kbI4=Yy;y2>2Tqi{wjv<;9ohkRihE_5ga;_hukFIVeEj_67W=;{D=FNuzbuw2&!as)EKHn@+?'
            'qN!)^S#B56pt}^VuE4{xdh?EQVzh1yIY9B`RH2G6p@(G{Ze_e4krtur9%-'
            'uYQlx=P>m$vqgKArrhn|tfF(mMtn`F^3)Q798B5P={k=!%ei8VV}uS%?b`5?xQ3ieX=39-'
            'x~dR?pFvS^!awKHbl(9~G2Z-u}Nh1Cz@{Qdc?9=|)OE*2ok2G(H-4?^-'
            'E>}9=1Gg4y&^y>MFN3u2i02QHW9(WyxNU1rHDd}=&FmkYk%><TC`z;KNDr@$VP$N0IHI~tg-BwDL3TmzV?$SAW;J'
            'aq%Nh93^MGP-'
            '3>aO7q^L;UXhviTg6YY>R{@3yk<3G9%Nffgh^Xup{>~uPwOdk5fZa>cSkK^B`adn$1q8buvk2B#WTt``@o`3^&v9'
            'k4UDPvTuc$8MoN?Xf8cUdb7W`;4>CyXkajPK(|+NNRGL+n_GV0G%>(c(rT(fM|H6z;4YQz>Wkd?MQc<^iK_u`-'
            'O?-'
            'C$2&9PvHo1lmo2umrC=+6qF+Hqw5&ov5p%uDNDdA~;0p9C@NCIwr}9DKl3UOSbPZ@PhXlg`2l8Jammq`cKGnm80W'
            '5y&|B7iBvtn+#?CyK4uER;d+8Tn(%RZ0EFpSoF;nPi=G>WP}&(3Z%vE{gW@g++li4=k>JEHSLi0+y!}*&6@I?@z7'
            'HKY9?6w<?c&Tptw~gDuQMz8lwp6r(S2R>v`kryCfb95Vig%M@AWr3eP_9pwmx-6w=7g4QojTCd*}?q%$YG5F=-'
            'LbONLs*-Zpa)TW@8TMv%+T3x`p2t)0xD@KAvwAKus~2lD5)duNKT2`chqOK6J~l1Wy$K8yj7Grxo~Wn3A0DOQX-'
            '9WwUZ9^6>gp4+siy{BCg3DXz2%$M~QnnOgjBoobS4{Cn7fxPnan%iF&AwTTLJOFtL>{IonfDcWquPldqBT(q}zBT'
            'tFi4XV5&mR+~i4Va6?<Eme`p(pQQ6r1PNDZT{P4n_LRB#$**xG`gw7;gO9Kk{X?@N(&s$5{W%VOavIJ&|<gSv7wz'
            'X}tnMVgYm4n29KBOqJytqC@lL)RjuFE-kgO^T2%nIEI`=-Lt~t)$oL?COi0GjIx$5J;k}1W)|Mi&A%-'
            '%a|dC?d{2beix~l<xuAyZfm%t?v(a6UK!qLVWuQFhWyWF!T!McISLZ|m-'
            ')!z=<#dRE$!Hz1BPQRx~~+AaTyEdieIaqWizdrwe#iZs#u}PxP4PTBKm4$m0EzImdH!x7HLmA20Ar$yh<xB<3@zh'
            'Rh5sC{#|M7pwm>XM(9S3gmv=F_kUf4t5SELfo7Td0;##GK(28DEgH2gRCKE)ckRsqaAbGk`lbE$7QM3aKe@;N9&-'
            'C^39yUYfVd0k7SGKV9;=<6t0BKqmsS2r06L2J@LvUHLsb+;B_**a5HqJDT<U<G97PQdmM_<}QVR_tD<U`fq3`HER'
            'K@>XrY;P}UMY+%WUN$<f5&|u$+UW>R9ORh+tug5Q^A@mEBW%kBC$!>1bi1CXTjVW+Dy}PPeybN1bAcf89HE6&9o_'
            'H#q;Gq$~$+UFjI0)@Y6uuNPc%;7|28hZpO40>M~7vH3v5qQojAtTI-'
            'i*zgyk**0Tso;=Sx!ykh!n%(5uT(kpl0Lh!-'
            '|MRcL%pi~r(3)LIZ<u=XwGdo^nW{2~>YiMx1kV5tbSEL;#x%|Y+0{OL`P0U94r_rFFF+#JjmRN2tTaw1M5Qwcb2Z'
            'Ak+K+(1QVC&uFfx9Z?;6Le#Jbr(R_1*K=XIV;Hqeq;Rz_c8D!`RBR)_DxBw;MJc6GiO^y=;GXQl;|~7gwnF(1V*?'
            'a<$;Jub97NXFCpAYq>oUHtp)sS1)dG%#mWWS|gqigH55Ds$d~!1G60<`lO0r>J|p<b_G&DANU<zt`(3SOTN&jOp^'
            'Q$CSR~*7Aw0q+S@7M&rk7vXApl1Dfr_A-'
            'F`yuRswGJPr2f=$`#(k9VOegKk~RGS6`~|Z?@{m8dD$SL2q=5apvIz=s<*=i~06Pz$o%{Ow_t+8`D09d+x3KX(6e'
            'a>z+A5X|3;CF9T;>1rw!>{Q_HqMhf5XXl!P8TPtK=_l!<rKE(`&x$xCOp`8tU^e2|jBOS9#uJfACzPaoDz2p7*8{'
            ';0Hk4W0^h{>PWc5+p&*c>q3fMCU>BN{8yr{Wv1CW7>$;Y~*FM;NU4Ra2d#J_74`NUh|_C3UAYlM^TEbe`hj>hO;='
            'vOYtLSFbOT^OIFx+w_z%v2~|aW8f$X1PjxCJ7Vh=j1MIt=)6A+E;`28c<smABIWnur6SPz#E{t%Dv#t*2Zu6|ik^'
            'OpS{R)TY{Pb;v2HBVa{DOQNa%~W)GpWjN>t6SgB$x@8?ma=Ee&=XuB)qLPpQRglQn~+vX6?;cMSbVqQ&|Z;~hkur'
            'WHt@QbK_Njp+&6%3Zlzm|txcMsv;v5gANHXLO9p;yvcK875lX2SH7w>DD<tFnkdmV(<%PjM?c&sL6{aiRRHyIN^V'
            'QdWkGeUP@z>BGG@qDkU-EQWAmbG2a+=X_CQLBaFyNhusM?Ey(Qmq8*c|tZa(K4+ho<*{J-'
            'mgd2fn#|9baKlQTSqUV?xWYlb?)9S-'
            '$4ARcDo=pZB*7;6x`DwsEM^CK=pyTIJ2HY>}L@3$WMXGq{&wnfAGKlUr=;gcZ{}aJJDS{aQW=x7ATDUdSSJ{Vai*'
            '(`K-&hmr)tI!Dl7R}8A(Zf%eO4``s|oAUgS8fDG)f#=jxC{q?qMypUl(@D5wz%&-'
            'VuFv?keqZhSy28DrIG3a>vndbs89W*sW2syN>4X;NO@=1I?KSq_g0HE_wa#AP_C`cN5A*Jf7*hNeN-qR?>LF17=w'
            '6dK{FB6q6sY5A;Exg44cWsi|0obfRbMxph?iDqE_|+7u`lgxMa>9I)e$KoI!+sI&mI+6y$wr+_A#6{=Ly)Da6f5g'
            'CPETS>_V;mkZ}szV8n2d2NeqWdC=8Pdlnch3U91QJ5y)$@o*Htg|~X2Jcs39C}?o#hC|w5xkd)+yu9_$V)`1y(P3'
            'vRN^?+w&cp#TklXD+2?^h62Kw9iZU@DyT+R%K!?+XHiZDk<1t8aMj+0BUeNz2Ynsh8Y?^ti0OLs6nz(Wnx86+6Vj'
            '=dM%a%ejY-#o8xxGSTdWVS+YE8Gm(oG+hRRkA%xOM>qX}BUa!YCkc&|YE+?<Djwo2dr$Kme37rTGm+x_Dx-'
            '#xpB?#p>9am5zF{Vj^hXeo3}xi+KFbw=I|!92MS)cquOrhJI*S?=%sesXJWG<J|TK16N}K4!FBT=Y4(sCVR+_N9M'
            'NXUe<VoIau5seO5Ous_||2G!TEvD-#<4l>7z{Th)&>-'
            '1?9{%=g+0tT)v0r#=iul~r`ZUyVIgtc44?rah3WzF2yGIl5H*vDAN?qHMkEM@92?_fgtn_9lNuw&iHo|X0(=I#-'
            '9N`JJztnp<Qe_Kl0eA(u9{uuymKhAv*V@v;fPqJt`uj4TPHvG7Q8rmM<QXpdEL)&oDY~>Jd!{D?93h=vOgCpC5i4'
            'Mwf_YRzdo1GS}Bf0w+uN=5DF&@i;3p_~{mZR-jV^>dmlooMi<@(^%zTg|jD%#)yXYPqMBB$ho_LoL@wH^#Qp6V0V'
            'RV`-J>U#6rsh9Y%<>l{l>kqmJ04qXt5%B}_)R_ZG`;rc~ikPT)+Ec#tWvH-'
            'F)~g_s9E<YMeBy*ErV93x<yNr=b>V1}m5?%hUISL<@QSRjE&br2g=)J>BUfvrdAy03K}_Ik8J)kg9<+eF0Di>Z4A'
            'kLbIw)!?4B~R(kBGIV)wtTen8yMtU<I5aw~Bl@gMf?&Y63mjj8SxFGrf9zaN%q+VMmIjTHw3lK&ltn{1n<!Pp`!b'
            'O%S7^H{8a$4pleWh^PdYERZ5XyEylks=PbjG%;x?r2tn<7Y<#jX(cn9?V3Ox;dE(aEgGrr?#+uN%hJV0F56wNLSF'
            '~hj#~6F16EwsZJYTz>##K~Wp3Moq0N%C2WgAlGW~DnY1L*>z=WkS$11@qB3?e0<>&g|{<|6;#`SzTD+wrJPrt|F7'
            'LsDqJk{*h*%w{QL6gPUW!PXuIqIqWg+`&tBA0ZEhGc|;L{<WtCh;K<g-'
            '5#gX^eH<hPrk$cVE_~<G2X@(5GGyWv*n%!#%>{Td<g_n3*-@2;i->P|w+cW4$e|5&r~>XQc&-'
            'Cm?{`dQrnx_bA(IBV-'
            ';ILI0n@O759heMsEN=<4_<bQiz%e(~_nU8^zV{uZk4k2L(=L2Iy8M1FfTzE8IW7WOj&cNv1?0)L1u|HBw@BSh#2j'
            'w*%Y7;@?#`j>6!4V6p`n#s07c!l)F5;)neSVjM7vrk}Sj&e93X;^j&AyJZ?{|>fgB$L3UtT49LET{6>EXLbde+`U'
            'q-ILvnMt3&XdZPTDth6#Hd!jt7BAIR!y{NBZm3l>v0HVLKYoy<a2(#`6+B5m?!*xbx+~0{SkkqEFM6F?sLerG1bs'
            '*>0PE>nmCMn>4F@mE`A#SP_^S8X8J#=e9bGI^V3mhebcGw!-`7nPv>%#U1<~vy%`dS^jt-jl7#J9BHhBf7isDy(D'
            'LW18``tW`mze9SXEzK~VIYw<fY(`mMuIkOjWiOCOiwc#0`%XAdCC`Wx1KxiQFM5}Cr5|qex3;uDL~#}J9U<#ORk1'
            '9BF5#iF+U-%#bWUjqjw(eI2)p&Ws7|vTl-'
            'q$Z4#M7+oo%f<j)jMxly;)RwjO>nS{q7(kNDsA##@?HvL1rOC$WzNbsIg6BLCPn5tBU$vnF8$?>}uR|Fori0$U10'
            '>hEesA$v*Wg#Kwp`NuV*+}RBB|5?(dc&L8#D{?0^Kt31!+S&m0HzHY{j#L4(r)BF#AJpBgR@<Owf7JXqv<xZ#qv&'
            '|oSF|17wm>z3X6+`kHlx)?84mkf3#C3z1krP%vMud`7Rvo??Qo=Y{%>uD(>Xmoqg!lB$Hpcqm*=%8dY-'
            'G)^{ol;R9u9teBO)gw!4HJmA8nui0aG!ndIvqBgt3XmZt(Mkd}%?L_#YVnb0WE=HiRvNDMbKR`d(7_-'
            'H$4*M5IFeDm_z%OCa))tg8s-U5KO{d&L&0-'
            'z%~c8_3TH*K?|Cc6HG%)y)kQrtO#^XJIf+$V#IlgxRmEJNuVN#+#XSz;91+|_lP<Ti<ii7>7D%<MeI!k`n4kGo3_'
            '<2wr;GI?JBp9N-'
            'UVEEhD=;*vrq^P2U6h0s&{(C<;TwJ$hk!gF{oGs#bqhgFZlwQIjg)y0G<s<uS(JYC(!bUrshlVO#l3xTCy{cr3W?'
            '+OYg_fG85<}R)&DE_Dg!L*>!$>kWCW(Tq;mHE2pSU6;7>3uYmM|e(Kbqmt@jxTzMG1$FlB-_VFv*|2JUKpkeERB5'
            '{^sb1XD6p`{+u74p1yhZ{ZFSy!{qH51B(Bf!;g6yiZOPk)Mwxk3)$3DI`+h_7R(Zm)5|f$L<vR{wMbYn9#NN2h=X'
            'k|>nkJ#@JKiQVPe!4?m2R@|Ay=?(p-'
            'Iz#jK)o!b;h{1U!TVV`UxlQBUe~BoF#vSLFpXBl(C9^p5A4S%XRKJnw>kYwj?x98X*t<|s)B<B<nn<;Ch^Ge_9QF'
            '063E@(}i8k=7<<z*+K=5Oc+p`=KIUBi?`o8ckQWUyc}7LWr{fP2lRU>T9D&xCOS%Y>SvUu)eH{3W$#Vjkp9L_3R6'
            'x@EElY12}^B`^ic9+ol9=@hwb!W>?E`PDLFV{ESo+CR3kiFrN9hHG1f+t2qwCf(H;=cxyJ$;Wq<DVx>9V;vBjeRo'
            'Di46wxY9QgzdjF}i^47vg=buNIBTH;MO_s4RZ|diM!4P_W8La(>MP7S$}H9o7JF#cE^+<nV`rIEyUO81viUg`F4I'
            'tb?7EQ%om4=M;667%{oJq*TxV%GZZuC5(Lm<N)9`kz!i|{GKR~HA<eM(}yAx<6<^DFUId0pdIkpeGkNNxUp4nwW~'
            ';<d?1ph7U9QN1~C$~ze##8l6MP$8Nq}%Z&7b*x>@FeA?+tn5!`HHD13Iqz)j`gTHwf8kZ4*7gU5q(&7;Jx7e^;Q='
            '06_3eDeG#bZ@;5Z_i>LU;1C<L}f3Z9IBih*>q<+L9p-'
            'soH=7_4{)%^my{x#Cnj14yt1?WNhGY{36a8u#x37(0@E~DSY$Gt*^a>myy2Z4*$luJB>U{vi`lhKAd0sRpMRng3H'
            'F--DvP`ymqo+n(F8Q%TIn4ZO~Y4OQicP@S0<t5F@I%3D75@Y2gjE+(k1z6pu`nL8b|Us^`0UD!_LZDpdHLl#IHNb'
            'w%xE#4+=_Jerg2KMr{mt;K9-CK(1C-'
            '0Jq$(H`qwU8@2SLDeSc<mhh~s1A>~~7Y!wdD}a4kU7$`|d8LvrPpoOQ*v!w%)vM{T9PgP>O^8Kcxl4D5-$g2>g-'
            '}xQeaF}9%X-'
            '0ZBI*mvoovQl(ok0eDRqxSL6I4|CH1{=7k4{y#)C^isE@c#W^Ap15EbDT_C2srd?&E4Y5GdsAD>?(LZXoG#xgd6%'
            '(ibVF1}Iv&WCu*c%p?a)WW6)Yj2T!!6&IVT`fy8bzQVxqL7_BE|?-'
            'BRPNd@;A9V^?wcc@haMA$kB?B##ALf%k)%be>8tOEt2QzpmYwR07S+Wt4xM(HOYS5pd+o%vRyO@-'
            'BRD=B_&zAMD<JrXOaO{VSzc)D37~Y%6l<-Q8?_4%pA3vJP@kMAW1ge&D9v+Zi}PG$fFvF{+xdS1zvw5&'
        ),
    ),
}
# END GENERATED EMBEDDED TOOLS


class QtRuntime:
    """Qt startup result without dataclass loader-registration assumptions."""

    def __init__(
        self,
        application: Any,
        pyside_file: Path,
        plugin_file: Path | None,
        application_was_created: bool,
        environment_was_restored: bool,
    ) -> None:
        self.application = application
        self.pyside_file = pyside_file
        self.plugin_file = plugin_file
        self.application_was_created = application_was_created
        self.environment_was_restored = environment_was_restored


def expected_qt_platform_plugin() -> str:
    if sys.platform.startswith("linux"):
        return "libqxcb.so"
    if sys.platform == "win32":
        return "qwindows.dll"
    if sys.platform == "darwin":
        return "libqcocoa.dylib"
    raise RuntimeError(f"Unsupported Qt platform: {sys.platform}")


def locate_qt_platform_plugin(pyside_file: Path) -> Path:
    """Check configured/package paths, then bounded product fallback roots."""

    from PySide6.QtCore import QCoreApplication, QLibraryInfo

    plugin_name = expected_qt_platform_plugin()
    directories: list[Path] = []

    def add_directory(path: Path) -> None:
        try:
            resolved = path.expanduser().resolve()
        except OSError:
            return
        if resolved not in directories:
            directories.append(resolved)

    def add_plugin_root(path: Path) -> None:
        add_directory(path)
        if path.name != "platforms":
            add_directory(path / "platforms")

    qt_plugins_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    if qt_plugins_path:
        add_plugin_root(Path(qt_plugins_path))
    for library_path in QCoreApplication.libraryPaths():
        if library_path:
            add_plugin_root(Path(library_path))

    pyside_root = pyside_file.parent
    add_directory(pyside_root / "plugins" / "platforms")
    add_directory(pyside_root / "Qt" / "plugins" / "platforms")
    for environment_name in (
        "QT_QPA_PLATFORM_PLUGIN_PATH",
        "QT_PLUGIN_PATH",
    ):
        for entry in os.environ.get(environment_name, "").split(os.pathsep):
            if entry:
                add_plugin_root(Path(entry))

    for directory in directories:
        plugin_file = directory / plugin_name
        if plugin_file.is_file():
            return plugin_file

    fallback_roots = [pyside_root, Path(sys.prefix)]
    executable = Path(sys.executable).resolve()
    for ancestor in executable.parents:
        if ancestor.name.lower() == "tools":
            fallback_roots.append(ancestor.parent)
            break
    for environment_name in ("HPEESOF_DIR", "EMPROHOME"):
        value = os.environ.get(environment_name)
        if value:
            fallback_roots.append(Path(value))

    searched_roots: list[Path] = []
    for root in fallback_roots:
        try:
            resolved_root = root.expanduser().resolve()
        except OSError:
            continue
        if not resolved_root.is_dir() or resolved_root in searched_roots:
            continue
        searched_roots.append(resolved_root)
        try:
            for match in resolved_root.rglob(plugin_name):
                if match.is_file():
                    return match
        except OSError:
            continue

    checked = [str(path / plugin_name) for path in directories]
    checked.extend(f"recursive: {root}" for root in searched_roots)
    details = "\n  ".join(checked) if checked else "(no valid search roots)"
    raise RuntimeError(
        f"Qt platform plugin {plugin_name!r} was not found automatically.\n"
        f"PySide6: {pyside_file}\nSearched:\n  {details}\n"
        "Run the ADS Qt runtime diagnostic with this exact interpreter."
    )


def validate_linux_plugin(plugin_file: Path) -> None:
    if not sys.platform.startswith("linux"):
        return
    try:
        result = subprocess.run(
            ["ldd", str(plugin_file)],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise RuntimeError(
            f"Could not inspect Qt plugin {plugin_file}: {error}"
        ) from error
    unresolved = [
        line.strip()
        for line in (result.stdout + result.stderr).splitlines()
        if "not found" in line
    ]
    if unresolved:
        details = "\n  ".join(unresolved)
        raise RuntimeError(
            f"Qt found {plugin_file}, but required libraries are missing:\n"
            f"  {details}"
        )


def create_or_reuse_qapplication() -> QtRuntime:
    """Reuse product-owned Qt, or create script-owned Qt with scoped redirect."""

    try:
        import PySide6
    except Exception as error:
        raise RuntimeError(
            "PySide6 could not be imported. Run with the bundled Keysight "
            f"interpreter or directly in ADS/EMPro/RFPro, not {sys.executable!r}."
        ) from error

    from PySide6.QtWidgets import QApplication

    pyside_file = Path(PySide6.__file__).resolve()
    application = QApplication.instance()
    if application is not None:
        return QtRuntime(application, pyside_file, None, False, True)

    plugin_file = locate_qt_platform_plugin(pyside_file)
    validate_linux_plugin(plugin_file)
    if sys.platform.startswith("linux"):
        selected_platform = os.environ.get("QT_QPA_PLATFORM", "").lower()
        has_display = bool(
            os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
        )
        if not has_display and selected_platform not in {"offscreen", "minimal"}:
            raise RuntimeError(
                "No DISPLAY or WAYLAND_DISPLAY is available for graphical "
                "Keysight Qt. Launch from a graphical session; this bootstrap "
                "does not force offscreen mode."
            )

    variable = "QT_QPA_PLATFORM_PLUGIN_PATH"
    was_set = variable in os.environ
    previous = os.environ.get(variable)
    os.environ[variable] = str(plugin_file.parent)
    try:
        application = QApplication([])
    finally:
        if was_set:
            os.environ[variable] = previous if previous is not None else ""
        else:
            os.environ.pop(variable, None)

    restored = (
        os.environ.get(variable) == previous
        if was_set
        else variable not in os.environ
    )
    return QtRuntime(application, pyside_file, plugin_file, True, restored)


def print_qt_diagnostics(runtime: QtRuntime) -> None:
    ownership = (
        "created by script"
        if runtime.application_was_created
        else "reused from ADS/EMPro/RFPro"
    )
    plugin = (
        str(runtime.plugin_file)
        if runtime.plugin_file is not None
        else "already loaded by product; search path unchanged"
    )
    print(f"Python executable: {sys.executable}")
    print(f"PySide6 package: {runtime.pyside_file}")
    print(f"Qt platform plugin: {plugin}")
    print(f"Qt platform: {runtime.application.platformName()}")
    print(f"QApplication: {ownership}")
    print(f"Qt environment restored: {runtime.environment_was_restored}")


def operation_specs() -> tuple[tuple[str, str, str, str], ...]:
    return _OPERATIONS


def find_operation(operation_key: str) -> tuple[str, str, str, str]:
    for operation in operation_specs():
        if operation[0] == operation_key:
            return operation
    available = ", ".join(operation[0] for operation in operation_specs())
    raise ValueError(
        f"Unknown diagnostic operation {operation_key!r}. Available: {available}"
    )


def choose_operation() -> tuple[str, str, str, str] | None:
    from PySide6.QtWidgets import (
        QComboBox,
        QDialog,
        QDialogButtonBox,
        QLabel,
        QVBoxLayout,
    )

    operations = operation_specs()
    dialog = QDialog()
    dialog.setWindowTitle("RFPro Diagnostics")
    dialog.setMinimumWidth(520)
    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel("Choose a diagnostic operation:"))

    combo = QComboBox()
    for key, label, _description, _filename in operations:
        combo.addItem(label, key)
    default_index = next(
        (
            index
            for index, operation in enumerate(operations)
            if operation[0] == DEFAULT_OPERATION
        ),
        0,
    )
    combo.setCurrentIndex(default_index)
    layout.addWidget(combo)

    description = QLabel()
    description.setWordWrap(True)
    description.setMinimumHeight(55)
    layout.addWidget(description)

    def update_description(index: int) -> None:
        description.setText(operations[index][2])

    combo.currentIndexChanged.connect(update_description)
    update_description(combo.currentIndex())

    buttons = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Ok
        | QDialogButtonBox.StandardButton.Cancel
    )
    buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Run")
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return None
    return operations[combo.currentIndex()]


def choose_analysis_name(project: Any, configured_name: str = "") -> str | None:
    from PySide6.QtWidgets import QInputDialog

    names = [str(name) for name in project.analyses.names()]
    if not names:
        raise RuntimeError("The active RFPro project contains no analyses.")
    if configured_name:
        if configured_name not in names:
            raise ValueError(
                f"Analysis {configured_name!r} does not exist. Available: "
                + ", ".join(names)
            )
        return configured_name
    if len(names) == 1:
        return names[0]
    selected, accepted = QInputDialog.getItem(
        None,
        "Select RFPro analysis",
        "Analysis:",
        names,
        0,
        False,
    )
    return str(selected) if accepted else None


def embedded_tool_source(operation_key: str) -> tuple[str, str]:
    try:
        filename, expected_digest, encoded_payload = _EMBEDDED_TOOLS[operation_key]
    except KeyError as error:
        raise RuntimeError(
            f"RFPro diagnostic operation {operation_key!r} is not embedded in this "
            "launcher. Update or regenerate rfpro_diagnostics.py."
        ) from error

    try:
        compressed = base64.b85decode(encoded_payload.encode("ascii"))
        source_bytes = zlib.decompress(compressed)
    except Exception as error:
        raise RuntimeError(
            f"Embedded RFPro diagnostic {filename!r} is corrupt and could not be "
            "decoded. Update the launcher from the repository."
        ) from error

    actual_digest = hashlib.sha256(source_bytes).hexdigest()
    if actual_digest != expected_digest:
        raise RuntimeError(
            f"Embedded RFPro diagnostic {filename!r} failed its integrity check: "
            f"expected {expected_digest}, got {actual_digest}."
        )
    return filename, source_bytes.decode("utf-8")


def load_embedded_tool_module(operation_key: str) -> tuple[str, Any]:
    """Load one bundled child as a registered in-memory Python module."""

    filename, source = embedded_tool_source(operation_key)
    module_name = f"_rfpro_diagnostics_embedded_{operation_key}"
    module = types.ModuleType(module_name)
    module.__file__ = f"{Path(__file__).resolve()}::{filename}"
    module.__package__ = ""
    sys.modules[module_name] = module
    try:
        exec(compile(source, module.__file__, "exec"), module.__dict__)
    except Exception:
        if sys.modules.get(module_name) is module:
            sys.modules.pop(module_name, None)
        raise

    return filename, module


def execute_embedded_tool(
    operation_key: str,
    arguments: Sequence[str],
) -> None:
    """Execute one bundled child without loading another filesystem path."""

    filename, module = load_embedded_tool_module(operation_key)

    child_main = getattr(module, "main", None)
    if not callable(child_main):
        raise RuntimeError(f"Embedded RFPro diagnostic {filename!r} has no main().")
    child_main(list(arguments))


def run_operation(operation: Sequence[str], analysis_name: str) -> None:
    key, label, _description, filename = operation
    print(f"Launching embedded RFPro diagnostic: {label} ({filename})")
    execute_embedded_tool(key, ["--analysis", analysis_name])


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combined RFPro diagnostic-tools launcher."
    )
    parser.add_argument("--operation", default="")
    parser.add_argument("--analysis", default="")
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    if arguments.operation:
        find_operation(arguments.operation)
    return arguments


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    qt_runtime = create_or_reuse_qapplication()
    print_qt_diagnostics(qt_runtime)

    import empro

    operation = (
        find_operation(arguments.operation)
        if arguments.operation
        else choose_operation()
    )
    if operation is None:
        print("RFPro diagnostic selection cancelled; nothing was run.")
        return
    analysis_name = choose_analysis_name(empro.activeProject, arguments.analysis)
    if analysis_name is None:
        print("RFPro analysis selection cancelled; nothing was run.")
        return

    try:
        run_operation(operation, analysis_name)
    except Exception as error:
        traceback.print_exc()
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.critical(
            None,
            "RFPro diagnostic failed",
            f"{operation[1]} failed:\n\n{error}\n\n"
            "See the RFPro Python console for the complete traceback.",
        )
        raise


if __name__ == "__main__":
    main()
