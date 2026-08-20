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
        'cdf8487949d1aae80727333c2fe79b5fee692e810ec77e05515dd8916dc5efa0',
        (
            'c-'
            'rl~>vkJQk|6vaPf=a|&NRvbAxdt0r)kr@Y>9I7tS*#D+uI{^tBXL9tQLTRQGh5mhv)1=e9!Pb*gnaZ5s{b3TUCLQ'
            '`m$$c_q4@AULzwT;~r_69xc}8s+g>+_vP#+S+2_WRe7CUmi4?`uWpiJF-'
            '@A{eK}2Dl+D${<9fAjlIFTBm&vMZHZ$>8wMgDPJ6_e}!Qjnik*u#O(PFZymTU1-'
            'Q%y_psZ8o+Dcgxj>c5tg^*A|NC*_Bwn4-'
            'ZZO*s>v%juw46tkPAYJS@!ivm`b{N*ppVpWJGm8+BT*G;*Yl+9oMGD?c&a#od1QZLG6Syzj7Qi%VbtgE@0wT4j#v'
            '^O>B2zRt9FU0DvL`Pham`86Iwm(ju)vKhbXRz-{y_i<(s$Phlt_PE1krcD0PG)s6#j(T=1W@!q9<T^Za@?17(p2-'
            '!tiS;W#i~putFjQA9wlO18~E>3fB`><HPm7UtLv&MlX*R@E~;`WpnMA8TveBq0F&C+j)qTiQLkWzCV|n#?CW|ZR&'
            ';$;E)dG%OqQZUy&6nrbyGIu1jdsGCg!fr1wO0+8K$)W(4t=Bp0KYvxj~wygTckBo+o*Ju~~0cWu7P193fFGL?5}q'
            'f%>+(6bo!h_4n0!K2!g$#G==AJ!{m5d9l7y|E~4dmG0bZ&c#9m2I$|K8~sl>dRp1ESQirk2eC)BH2sNMEX71(zv|'
            'axm=}Lo-z=-'
            'erTTubxETpt6<|4^m80Z^Ksxd3C{dU=7!1Bh4h51B?jxiXI>3!MA=pmp`5X{tf&dbeH*iFkn|ZldH{-'
            '$6!)FISK0nP5ULHLE^U2Xk{_^0(VX~hHNUNXz<JGGd`RS|t@PD2jzC1k<KRy$<Sc=(SZsy|HlKLW<3cL_lS6l!pz'
            '?n_UNi_#V!RsNABRPKhjNyAR+mv{TH*>RyH;2cs-kj#g2XDk8P7mMYPY<6Qy*PNDA3r~MatJejHOP-%o*W-'
            'OIeqm;H2>k~<n+y-'
            '^MljVH%EW`@e~)HuP($n<wz}ZHDRvtuMsFT`0x5ih63_`D;N8xt4)~=@KbUEU4McV?hO+0e**1ZiJM-'
            '+qT$jg@<0R$w}N*PAh2o5)y_pRfrDI?g0M9L&WM&{#9kOrUz&U&{=1hn>lJ>-'
            'k@n!=@y}`1EN8_H{oZTM#{g`5%}D6PlFdaG2ytF5a7hWG9Z)f~BZ*sVtuUm3-'
            'n9I%Cyr~4A5}B=I~&^li4J@(S#OrJ@~wgJC>f8(XPw)7y%s19m(1+$9B4v=fS*>y<)UuZ)uc(@l>+ID8SDnI4scN'
            '{YYD_nJ_O=TSUD$x1bu=Z4g8lk@Qmaa)l3`;-'
            'ctNJ+XxcKz9#=E=<A|%$H}jYCYMxpFF6;K23wSi_tmOi!0p2pic-oZU2yn8;`5slXvA@GX`?7&<PP1r6*dtEe`&C'
            '@Uc%DEwWQ}m;01w1T-'
            '8hW(DxWlsUxi9I{BXGf+E5?G#cYzIZ!ztK$BvLWV>9g>J@e&T7y_6?#ZUfXT^CrV?T9)1Rgzn^WNZ-XTt-ZMcSi$'
            '5fv!J?V8l@%a#3X!b}DZ=F!Yy=W2uObG=zFH*1D7>Y8a(r~egQN6`OF;=2UgRsK%g6WXi|(yIuDZ5GA*qME^*AaJ'
            'K>0AaTW)zRX;K)`x+qoH+DT!`16-k9XPT#KV$026XiU2XtIMC%YS8pfV+&^GKoNmj~(k8GKr-'
            '{ca>IF!VPk$avN#Hywd>&rD!swRe}U}vu>g0e^Z%|g8YldE!?(-'
            'Osj>y~(Ux+NnvegkSzUdWB+f&|g*L&0WVj68ChB|G1{JC?^yM+5%{bWA+o(@Gq!q`4!7&f*1yk;fijb#J_q7w!Pb'
            '{=T&st2v#NxTp&`&A|DJ=&1L~F%nmSo5ij5Jl#Ea0_-'
            'ug7BytcRol<3767L}qbQ7A5Yg{refyG%7*W`*WZ+E$xVXH59xM~r5TKF^8jFHO{_8py5BVB6<eZ+5Ap%FB4Q*V^E'
            'qKYXYBUy<P(bLqT3-#*S+&@FNHY&Y;)nBJKTOWYO`V1YfdfvjtHoE3Q@`)8;)iK{-HfNRS-'
            'khO5JJEr4NpC(Cv`EN-iUwG2&)1F2Kh`M0(~D|q(3g2%~C!!uf<~|hu=$X`D}No2HLEi0FDMg<~_#<L-'
            '>a#Vh7DTm<90wJ0+{SUN<A)0sse!)#M5}0x6vxJUw}M_yQ>yv@`Sz`J&^S6EWd8<Japa;)Pah`D^&&z`XOL<n{CF'
            'd{wM&jusd7fb$5z-'
            '3h|njtG*btdKdafIQ8rX8jiSbtXE$Wi+LjPIJ}rW@sK*1cXg8){3;7qmzQ=KFS|sVhn*>9cE+s<Ir5E^1}r9s8=U'
            '=knT``1q1uy(BN<x1l0L<tgh^bv3P6B#dN6pX7)ZM2;p4Xcj^Nr<4eQM;z9gIV6=jMliKU@2T30C)^c%pez2|v*&'
            '6{%e)ePdHnhITf5Xzp$JFy!uTZSc8PMJp2LbdNI;}IgDnR!cO+?EQC*We~cxG183>h^Mi{O2Iuz0KB&D9d*-'
            'GoMfVCJR@n5;@kX&oT5E(mMfSn9&Pv*YV^+SXq~h%?@Z4+2WV^z~`}`uG6k%hPAC-'
            'n<b1`0<CMmqG$P{Zl$h;Aj3Nv)^Pfln`abICV3Y!;de^_0XM443uVLA<R|lp=b(#YszKjJ<&Lx{}KmJ0o!s6&;W{'
            'FKqk3}Lo)3ja(ZRm9n)bfcscm*FbmNF-cqipn9a_M$va$e19XfX+X(OS5MO{*c~O1Hh_fm`l#|UG7zxoqH!)vbLI'
            'v9{Kqn`*0lPLWCE7I>o~x!v4#u<k8fYIrbf^b%NP@isMXmH0G=a^3oC}8h9e%l5mSUwBfVE;P4tk`2IzBu+dG#!R'
            'dh{mMq=0o{SQcCaf`+xvXpnLadXK9bA02m2@yxw>^`}=a4$X|FeXj{kbA@*FpaRPbjs1s9oe^GDaX$9oJsvAXP~b'
            'lw^I{1(W-Zt#3%TK`vgQF47r+!K0ZX=4P%YfOwhwPNc3(RDn#FeyAVXmU=Czl&x}4SLLv~#=pInH&Vei<Lb*?V9-'
            '42Q*$zPR|cgRnG_@mxTzBJ;)<b%X0(i!hBj&%*dxk$zDn^hy&GQk|eX75r9d2E<Uwy9hT$pgqs`pZIafaAXkwtgr'
            '_&QR)+t1M@NH%*6&nzR^-7o@SG{HwVZDPvw0Z+Xi$`<vBWa$S%#a8YlBXi#j{wScX7e`m9s@h^*%4JJ8Du~GI^-'
            'u<#Tk$c>O-Q3FE-SNIDXm&|!-'
            'aM3&C~(W;<xK+e0&=(I2f^Pe%?=n^1eF#4JEmbYtBsHVW*bEe&1Sp$Er;ilS7%#!W#FN@6wdaUVtu^YENr3gZ91D'
            'yQ&gSsm1Som8#UpW_fakF{2=vBq=!Idh}~c<@Xz@ysi}1n5^=VreI<hO&XamGQ*1CQoJs1j@C6TBoIQ>wL?4ni@G'
            'q%~V9fekJ)Zz<DIhJ5o>4vG{T9T{Nb$5;PsMhV2Z{Mx3@#ZEXxt1f7CF^Oo5C>A0)IYJ=WP~bb|1care)R!C!5@*'
            'uhpHgAT&zOH$b9)-Bh4}BDNE(ZeU=N>K*%{q@D~;`q#W(<*RZ77lkQkNe1^7%Wt41-'
            'JYHLdVzu~TE%EEdHeKFbnOc9xn7o_A|Og<WJwF@mCc6;07tY#{0}JQd!d>ILPbyniB{-'
            '$t^`&=ViVUuN=uyGXd`NpI!7Y5i~9mi>A5(Xnb_L#&H73#k5QBnPIYT@X@V4v*-'
            '3Eh4$0O(S5v{DXj|E9CbSG(HN0XARqq_X=DEucuu}#ZjmtseTCRbK8)`O)H)i@APwSyEWms_OpDk~M9Y<sy8zrQ9'
            '9r&zwKP3k(u$xNDDYnufDVuk0^gSNO=!ixsNimXb)+1dNz%`+vN{j)vfuTFl)1wnH$e&YWtlS@eKKS$VgO^Wp-'
            '6(UJG(H0=p1rk8t;20vUt9<bFUtiic3v&O0-4@9yk*B-!u#~HPUM1M&CVJDOSH-pDe&d0SYE+PFI^Ix>x4r-'
            'FE$IoaUk{=tVbi>J%LEy+80#Wz{Tj3GST}2dwe;zN0;aSUJyqqI<-o**cdENO$m>$?q-'
            'RxgtXw5QEwU_H&iD&EA!)9^#ce1&Xa9POcqUy-`3&VGb!nT)4}Y<66fR|?9+{`MQ;V9TK#XP-'
            '6j6e02cm^jXYk~OAP|L^YRR|+rxfhkSYc{)WEZKsWZW)=wp$%?Ho-u*pe`@gCN2*(u-'
            'AZrMB4sKidqY(*>Gt@TElQ4op~kd~#&|4ZE*2E6Qbq1}&R04Vs<F$;5$9b2Xzi*C^3Oahz6sq6u*X0om|6GtQjiF'
            'RjmKdTO-'
            '5mU|FNIfZy7#6XE&y%CymaTbY!9m`X4<~4JpsXIb!F46<JqvTeJ68ip^9|Y9L$$=&}YDs$m8uK6lx<{NCE+umag{'
            '!r34(Y9TYG_BH<JH{YtW=`|20z;C9Ci0>&<=_8M4)}x5d|g4rb%{o)UkH~BLW01^-'
            'Qj65Sb#l2kfS}7vgpKI4rcsfo(9beHQ{-@J6@`%6hR-'
            'M++hAJgtgZeW?^R^kj|%$^(~)6pA+k%5=0Y=jKe1lVM^f-'
            'Vt;N&^`#sk@BfYSxbe?d+a0b+x)p}{>el(>jtZJwqIg>acG0^fPfG_0S0d-'
            'SXOm!+d&KzOhG8)(($IuK|CB9zZ~0ahr$AmT!8ZeV5DMHKu%j+N)2T~Hm33exC6ms5BRXy%*$0ZA;%bIc_KGDaX#'
            'WminUnUdvcRW<u9pvakO1`hL>R|f6rR=YPee1uxvfdJPn!_MC`tB4F}F3xHMz$RQ^%Y_ljJ8hWLl`jEFzvGa?<q%'
            'yzN4*sk`ZK#I}0+g1)_A%@*JYVG56w9dxjEOnb8g!Hd;C}M4SbfMz!<My@cBQoQ#Q{n?Fm|07$8ZETY&xo>NMf_W'
            '8an=P3z(B=ZZ3z)Rn|jU_gC0Bi5gT1QFd`O&SPO9(j#uSHxk}J~ZUveU?Ov)qO3%TcL)<ZNWddhQ@of(7G4u24aw'
            'B-'
            'E*^RkXpY;H}YbJq#Fb^JT`%UBBEzbfQ7j&}_I>>igL*0F=U9{1IG0d4&7i=xTn`SN7Ko}8Cf6qcIb9><e?Ip)o>k'
            '(&SKFJdkmCg3xXM=5e>lG;MCd)%^+%}c}BRIOO*8&L}hrSulIfK%NIEom(6i=t)ZwX43ntYwLpQiM+qL=r&n$42c'
            'hPf=thY}@jwTiKESBC{0E&ypcAVZI+#(nbfLJwqgkHgN|iBi3gn)4Ye>nbgD&)d0e1hRcbM||r^iI1TGd1xmJ)?9'
            'soR7M<)5b@FDTTafrvGg-DGSuaaEs5BolC<}tznB=?fZ!^mG+V<;&TnXhpvBmzDg8VeMN`b;Un0-'
            'upudt(0{HE+$QP;FesXIAQ1H2r?m#yJ{KaMg<1r^+#rU{#3T{Dfx_kbh;izj-'
            't8!Tu0&@*2E4gOu%PjUf&Em$zbV`DU)qp=|tqeyH>X9ezlWlzz*z*Vvi40F05G6Z6z^Q-'
            'Bv&vpn2ZZk3Q0B)WxgzLpBQupU=yLmxcg0$4fn<WI$-5G-n|mFR2MFCkr8EdH3=y_tB{Z+vr3c-'
            '&!Gn~*ki4~??=7C?Sr$Hg^fEx=W!?%+xgy753@MJjPCItGKJz2XL*JT1$E=Kn@G{*@*26F5_A}?T)K781krMvTIN'
            '%TMXoP(Rn0*^O`|`j32F)SbJz({0GlMwR(;E^!MDwbI?<Mp4+y^FthRa65#`eYCcOIr-'
            '7w?ev{bLJuq;uGpe0#^$&#aeSKC7KtEbn2qR9H*<bytA41!MXsxgF7Nxz25@Xol*MR{=@<p>I(SHfVtw-jbAS4{H'
            '2%QDaE#j>U=Lw=n_lPRW_gqF6RpHD96<4g!iqzGPS(u60^X)|xKK1sl(O)EAQu%X}oelGZ%!3;G{ceCi%b<#{LJA'
            '@w+lJ!ZNoY0Lx`g1`kFi0&X(Y$nzsi86o=`aNJNsczUNnH81vNz5-+gE6(#X|j3dSjy#5-;&0R0YK>(d?@M7-'
            '6`esaye7a+|t~0`#jGJf$P<x)aSkDoa87Fx#GAlpw0%=>_Vg?ROdhuOt_jvIt}B(Fhq*o_&_LE3)UFwsFXVb0^VN'
            '6g1FBu*GvXUvEXM6n0h4R2gf)B_vUns$htZ=bi{`pTiPCJJ?OrKore}YAQ&4lQp^3)lVh5kmlx=cZ6b&@e~#)%>w'
            'NAFd+#V)&OquwNTxF(hnpqZZKa+fU{N9d2%%)?5bYm~*|`68vAQfxpw{t|Qs6C(OukhT9FwbJaVb@fv?mP%h#40A'
            'Q&U|oatmLTBE;RbxbQi2dR1uIuz4m(#8VvOL;zVTNPNAm)|7-'
            'N&9?Aqh+1fvaRf9!2&RLlC&}a8$KND0<qlwiV<9mbMTCg>Psb*Q+1T<ZL0A?y;9Fy0XFx_jS*jz65%Rc9Cu#~{rk'
            '`j|vkq7PWI@&%^rHYOHxq)VMms_{9k=U%lolZ%8Q#ZG1}&TLHyfnv^$6q3$OfUd;cQl5OZJIRPI~ty^m;fPjl&lV'
            '9LB)XM!qSFsZEX6SH+r?GUp|##s#Rv<DufOC1fRdJneoi)^Sx&eKZ>Lt;aO}7B<);ewO>C&+|FhBDLYbzZ|q(i@-'
            '~j%I%#+jV(sWRYn*K2(wej{ShnSxroR{9hTP%X~ptobfrfr=gakt8jb5v<j&qgd)SX`!cRnPKF*M(2kT^37R?&j3'
            '0jN3SY}aGqn+LyHeF5;W0~@GtskFH%RYtpWr!Iq*E|IV_~vZR=hYg$#>`czIcpia8NKd5s6=|cvRTWh%uCGXIW;l'
            '&KqWzwaXg3BbW@`EnARIX!OvnyYr{i1mCa~NvfHG4YAJ$PSmUH<xgJ{Ivb#>!EeAFCN1;$Fz9_y<jlyz<U~uJSxj'
            ';P!;7hfV7_%cWMlI_fiZb0?Z}go1#gRq>5B(9V^-'
            'YYOW$6LDSCm3~!OF2YpH&l`MTVyZ!NHYtI2!x3@XPIavV#%2)F-'
            '0J4Xu;Cu<CcQ>#F$)er$bL)d+szE$vLcCGK0Pu~g16%;2p<*S=K=#9w*uSw=&(Ry5|QnU!h2kAE<&O!}Q(q(6A@L'
            '<jlgLI4shu*&tE8Plt&HypW%nZd*!u;DmW-fob7z~^Ncq^ZfzS2stC_aTsLa9d-'
            'wyD&gQ$sAa{C~yZO?Hnih9uTyK=5GA;IjGXaAu`mYtP2(pZGS;MlJqFF&qw|Wi&g0pmY94(PGYbdymx{26|xUNUX'
            'pOkBxOh%<av@2TJw6knU#`Y|E;d)z!zYY4e0OidddtwzT|y!RbNYDye!~RR}8Iuz3qHeMhilB5LY1v=j#|>ZmKc$'
            'KBiVb!BR7?-'
            '?$NTD_mo3yuoCw$RT8~P;}XXgCPnu@TEVf)qYI$aN9Wr`nu572w;y7&G^nv>qF|makOhnCHjaP1Mv)~jA5QhkihG'
            'rfcz)$m-HO4UDuQ#Q&y1POCZ(j^-'
            'i<CnU#sW!rWQudIh?8@W6m{IqMtC@GR9#P1sRhE+iE3gTK?#Gwc3KJG}ILoyl0bxSxbGl?0BYKmZ^4iv=O=(zgY$'
            'An}?QvO3=gUP9eR07`LLfTdc1QD#n)4tYBYa!4K`VIXq(j*AzmmE_Va;y>ha+$ebi&M{!Kz`wIDu>88tYs{9E>$k'
            ';mX#=X@zSH9Em3VS;Rh`%G#7nHU)~rGDt*;k?Fz7Q(o;-Mv&^+zIFO3||3V%7m-'
            'wuQC8azY;lY*##a9`%eqlWAGvg<LpLxCJ4U*9at$k+-B*5F-'
            '>!T~>GVH^T6EJCh9ca~SlLZ4Hy2nV!ZB#?y#&rPs`GN+Gy^=p}7Yf+Xurbwd#?5i0^*Lgp@rMz+yYYSB6lA8|wJK'
            '%!JoDub44vh>^1sYGB3yhv-'
            '7}`SIgY7K55L~wa?BB|%wH){#;~T6OBgsQPUzGED0m;aSO@ZbRqO_b9lX95;n+&DVAO6q({{P@pVoUp}GP|tGF?g'
            '<uO$}G++hXT$yF0%>dmwsv^NlBh!Mvzvz&q+afYDg6NQ;f!LX$(k9OBnjQc(uK5{;yQ4)`gj(EL5FrG`{J5ZjQAN'
            'Y2w5G}gvxerEXpKUbw-'
            's$i}}t|VF4mqcWA?5adQsbPBudVO^4!;Ef><0#4bZ$EiEgb_#9qLT*+ea)oXI{KBs7wPFE-II)`&-'
            'E3AX30?vUP?(#j*d1SYJxE!mL5trRj(polc2NmYo<MKXc1lE<EkNg!LVV>j0%GLF1lMohj3r-'
            'DV1XY{xgq^jC?~aCk1K=n~;5+JRx*9G?3&!#3{&&X4|=M5E0ZJv^v|aESq!0mi9fy_NnhUi~)PJd?|hFI|R_l38T'
            'J_4E3~IjqK!X1U9dJVV6<15$|wG&UqebGf%N>(X##4ZC8!-'
            '|4W%4#5T0C)ZHnRapZ>{;nO4A85ULG^QxY~CQ<Cf$4!3h%W}M40~XSIggm|Muf2U$U_YoS7+ug4ZV5FxJc8|s8e>'
            'bqnK3481bXnD5C^l&wun=Nu5M}pe#_m!DF&032_W~_O0awMyaiIXoVLju@lofqHChL@)N(fD@a&vQXCOO?^A^6|T'
            '8xAInt{zhVe+DOkvVK3GuRNmYwxS3>bPmL$w$EcCmP}2uz#=nx6>5a&fBMuR0~LP>F?6X#JFc=oz>1swofvq8iiM'
            '_ebF+bFt!HU?2vog!MRF4kA{mVp#)}OQ{c1lA2Mdp_0cfPRxb>)k0#-fl15DyD-'
            '(Q$>?{k$A{HLJkoi||Av~>?{1e1mH3)Ln*s>;G--p#uAhZ{a{Pw_qg&8PezRw6qE6b#c4jRZTsrhS+g+ns)M539_'
            'FgPuiWb`s5{52*MpYK3y_AG(OGiCDvO0c6S!Bsf}#@4)5h}b!JwdVPdhvr|HgMkqkXO7G|Oyhi$2}P}Mgsv>y2Gh'
            '^#pMRy?WX)2DAgpH~!ye|&RGKyTkMj%dd!H8O{3dga(gK~|_^r~Os`O{(G(}*eNdhv6AqC^>AH#V)6=dO!_-'
            '%{_cLHtU&(KKt{8$5+K4ba3IQ<}azpLkus*MW-'
            'u{y@`g%<y8R$Ssgjuh7x83XcP<($iD8|p{VSaUN5>F_DiDO$Do%H?VAfZpz&A&2aroC=-'
            'S!!r)b%wis)pjuxKjYu>`63;Mb6v2b6omF?W5+VMIPkSLi*YJ6><lkE1-'
            '#4Vo)^9j~LWj>Fm~f*gr``iJ_9)UdkZGvkE4;|?9WyL}JJG<(sH6g@csG8Fcz6EYi!`^Eux}4;;333u4v>**M^=j'
            'vWwPL-88;{Gmve!c2(4qGIe^6~fRqfKz!U>;`v(MLpsjlzqrig)*=N)u1R^7PY@e;<LYtBPN{-'
            '<A=^^+?LpU%Gx41UE|Ct|;lX29PWT^KI{)juJ1<0)~lhF#(f+cGjTQFar&A4>)ujU1Gm|&UX$4mW;IyX%vXrs_w@'
            'v&0x=DhBaCwX3csOFn_4xB}US;Ga!e!aW9>uTWwjEk#%GcU)gzHZ3zTS+ZqQ`HPCoTwHijqrL^mW*XlPkj%VNoZj'
            'YEoy1+bsQ&RK=KvcZRwa_z)(lXUYK#}daYRx)?%1-'
            'nU#1)mgHQ9VRf<|PpP5iJ3f|g`2?@Nqb)T%Jkuf}M9?8}i3YpAIusGXZugyol-$F-'
            'MEnfvNqwqO!=2b*7x2I$njyYEfsaF(GbnTPrL)a^p}UEd3?GeHZ~EOHpf7Flbg`6z@*0B{ip6C))GKx)u2ppb9eH'
            'X8x^b2~AdXt^E)k6$15yAPY}YK1gD0FG)IQ7a_hW|{&TVVSSJp@m_LE0mlVD0?Ewd=GL1vl}z#YjAjgnA`UB~egs'
            'kuXp6sID&BiHmMX?7$jY7hqk$E-'
            'w3deMR{O;$9<xXDFvf)eh{WMMT>L>_j)5|oW4;zhSizx#5s7dj^yE`LXH_S3>wU<P!5VhvhA2vPyg$WwI*FyOJ%S'
            'pOEGk!|PeUa^kDY^NBlSffKmF%r_d+TK89840}O;jl-1V}rjSfJgCr7ygORAp9GDak>H-'
            'AyGwai;nq3wiDuI$mpuner;CQiCEPv2g_%U8BQTzbUAJ|=fhPx{KI$q%3_)g|FHk|VCO&1GBUP~jBVCZ3dM}R?mV'
            '#GT<}hBUgbX>9sZoZIzBym^)f$respkxwaRXZ^|}xM1K&!j#{(wEq5OvW(DFLbe}M~>{40~H(G*?7obL2Zb=QAkc'
            'lt|rhgv08Z+#$6H~=;r`QKn=_E(%V)Ewsz{cusvgWu;h<jCJdeiYx--XaU|ewMkuMuR&~ag5b{8sfsK43?!s9?9B'
            'RPTnsgLkNs08uH(b9{O80#+j;!CN9i6H@$E1pT_u~kT(G7cHt+qvQl%3ny4-pkf$$iHWwGw2OLCnBahDW`U7G!{-'
            'yp{*O!;G68}jEjQ>2}tk>e7Mw7fMt`W0Q0UlGZGdgPS1v*tnZmAlT`^T)RVu4ivZcVQd8_$Erot=IIHxA2mL9yp&'
            'dC+4D>O$#Hsd3;z5D)2mj=M44-tHwk5J4_GokgEpwJS8y%aQuE@^)(}1auD!aBL``aVQZ2ZS&z44yI*snK|ZggF-'
            '8*_5!jhcd2B;sarWuOR|b|-'
            'Yms+g8wBJmOR6ybfp^;ZuV?!r0IU`ZJApC8ueg78<OM3g7Ssu%Q7>;Q{3p+kUNWX1OQ&FNSb;BnOv7E<pRa3%z?X'
            'y>KgD*3HXb{=A~<d<?0IGhDaaNE>V|{p>4V-'
            '9H{R>)hbCG(ySwQ2=t?emytK~C>iqAGcOSbdo2iQpBPD?LcS%&c1Nf46TKLVO{x|>O1|3N9k4n)3}1c4gkPh<)=2'
            '!YsZ0XviOF5fm?u8|zHZfz$Mm}M1GBHs_G|YNaG#3{Ag22x4(jcL&$aKh?!6y-7-'
            'v8B4d*UZ{5o&HRZDTSz7J4<F9&4uz~U@<Kk!W~-ybK&Vmmq>?7Z#|UT-;`^OG}~QFg8CWj-'
            't4lTmIf&m*3FI2FS@hfyRXnUfiJFvIL(YC;T^(X*R9QL(ywU9D#-'
            '&sLiTx0iRAo@azr^2GS3Fnns;rhU=IIEmW7F?L9;lP{ZjW?H2e@VS-'
            'w3v_UWu2qcn7~GM&oCoot$(sq_`o6>Ef4#fwa!j;@;7qt#3`_|AY$xUdOUqYZ?*>4FX;&v#)odyrKESDt<AC;0Wb'
            '@RE^)->teAujq8c(ySNK+Qc&?c)Rhb;LS73~3<h|w{q2ncGyG`p~G!)VASa`K;b>LQ|g2<3->IhiE05z-'
            'E_r&W8c#yhks%(i&9&D%YU&H*oaBrO}(;ehLw-'
            '12Mpo7G(!?!qxnttgT%ie0ES#mC1zT|qedW^y&Uk2BufAEoj}b`}IKJ>g!6ha*`L0^O9ex-UpVQ|GX;_q3#92bA{'
            'T9uQsyu?6Zo&Jl2VZYNzd)JVFfL`70}y1-%-xwNR~g8(jmwHvxK#o{K6wrdQQu!-'
            'k;_uc1!*ByqbvB;&ErIua?rS?g)4ketX%DXMknL`-'
            '*8ZNt)ka2Zkw)gkB_=vlN$hR&A^rH)8!fdAw275xZffYMog0<8VO}J`zEAiS@ReesO+s#xIl8%jB{0yoh+wO7CK%'
            'Y6naH9t6C_xEmj&wR{3P{s-V5zuTY_H0i5m&&qWZ$rB5i_BkCfG}E*-'
            'U^RQt;Mwv+X3aSj;*O5N4}0h32Dvs9Ibl@?&IFiyZ0u8P(Cah%^e-'
            'Sg~9H8N%#4?9d=At?k=?dY+=}QHU!QZ6`%A2+0=G%}fu11Pq@7)zyCus*ae0%*$6T&qLWDF49{9G*o5772WxKXCF'
            '<nr9{s9)u0STXMV)Ou{hCeRTk456_}c4{TA}6VW<>HEE=NULi`|^k6eXHX5F=b7#Hw(*F`eN*<MC2?=t^6O*Vo_O'
            '^5Vkn451_o_w#7P!WP`5Ka-wXj4aFJ_D+^JKyZ?ol&%-'
            '3OztNt)&qv1<0IoOy<h;p&U;ps_bbB$+B&OD1O_pm2t{^XNOnVH8<TVc0=u5r#vriP3FmLoIKS~p;6J;9Iq+poGZ'
            'X!_^!O!pB3}-'
            'DdcDnXDWz1{Z~*jNcHd@H1zw%O)Pg0o^d5C%+O4u%jb~BzOA21kXo*NZe!>rHn=C3Vfkc!cE*F(T7h&^=!#UXstd'
            '}==_=r9$;tX^Rc|h-dZCBlAD_0O<qUGI-`5ga2jjQpo6Qd8vpnR|p|Yu{jF}yD6nkwMg-'
            '(96uex)+Y;}2At|Gc0qpX+h7@3|32)yg;hpkvI*b)szw#wGd_2N{uwO@U$X_8|(uaEr7b9l^nFI<$%1i-'
            'gw558<~vVi`mk)BR|Xxm7g!M55XUFD~BV!qH}+f0GP1Hmz}mcn~L&REc3>scBP@-'
            '$cgK!chMn#GC%w0m9C3v<gzz#UL+nI{2B2i7T&h6N~{+N1n|UX>5l?hG-'
            'M*Wm;Tz^fb%`caqpsS14;&oT2SLWTSVFwVXyXYWfYvLlD97Vm2SeZ5&jJwch9O%OZq482C>{y6y&-'
            'Ru?Y#o5koAjwiew7QZ`_h0A=@G`lw%yUSoHKD|#boW}<vV{4)Db7bD4ZoLhWNAIHZ88aMzd`AVr>{JWqUbh-'
            '<miZpw7q7vgTuUpFeJ*p#i{OextA}JHznr8TCa*lQ-Qnh>lfu>^HAC}c?t)5hUI0z%v)3eXR($;2@$1&f;b~OaKI'
            '@*20<1}SR%6c)e@5hZXn0%`Hi4nXp%dc7nda=NUl;2u-'
            'A8BrNhztQx$zsuE@cMC`TV6{ysNb@=9*_sg?AO!YH(k0}aur5kXL(QiOBf5c`hViKpn`#4^Vg#8QNrJHFOYVjJR='
            'cbVZqDcjh6#!{|kW-'
            'K@JRv#wnb7kaGW&TLvglm=Oy;)#dN9Vjl3Dex;^|;WdBujEmR4cIP;84E><wRC0IX5`Q0c!g>ENvxt3+L_vp@U6y'
            '-TAyai~oe@=3i6A#)@}UF$*pEGL(d*$aZ_;AH`~-'
            'B&_@NOReFvjBbLD*lMk8dk2z9p!!;%;8Y~EnL$QjN$?6m8y6e#IHFe$vXEXGu#gss=H4bHv_fQAO?_(7TD>@sxmC'
            '_Hm5hJwW(KEcL_8sy$@B6Wv`Yp4Ne#OBa-Sz>Aw@l;f|e8R!Kiz@vc=<4%EduH4mrXdv)!~E<^?AACb?Lq?zs)*('
            '{j^Lr~{#NfMYus7L#R5#EQHEtdPTgP9MR0SRkzD_In$RB|uazKjd$*=p9R2M=G4ppz+u7iZlax%o%0Rkg3tFlw6%'
            '@xkioy2-'
            'DbL_zt?QgX#$b2&1w7CfU<{z5D!ZTrsac8R8N`%t0Wi#TU~$^uN&Q&XEJ7KFn@<H*X0kVSTD=eVdU$m5P@k@MBL0'
            'jcv$ypY7|6U7j@{0+`N~MW5ncD~pNG&T@?aZ74Mpp!M2&n7)IXQ3`%@9YDSR^{(wY4k7CDxD$D<u6o}L_FzAe=7C'
            'sluPkJSmlVci5hJy*x_h=cfHtkI0iV_-'
            'IFJoF=o=hEImg2mO7N<L-6lzL*3-SXi!8SL4+s5yzuMgmm{0!2J${|F`+!8(E0wG-ob#}^v**V;e8#d0b~=9casK'
            'S%0Q&JxpkW$gJA?XdaM8K-'
            '=5#rQnr>kaPWZpaK_4XM$mz{%J94@|_j4Pv{`?}56}m}V^S%@^O10RLt~hwV&x_SK`EfC;-'
            'j!6NR#0Scey$eIj9(<&<8zn^6fIVhs}ZHm7x0-ussgyuU=@^UHjxxU)vIbT_V|xn%-'
            'tS1ty<kPw<Jd#80wG3s$YglJ#TB?8odWaWz~nQTQ}d~$o_&>yQNt`b(4e$&WxCL3dnj}G*B-'
            'Cg84>s@kBU5>Yv8{*A>ES|6kO{=w-G-'
            'HyV+St~lz^fs0~$SgO%mLW^;IY5>U#8ib5?3!b?i=)Mujo-N1PUv5ybb&Z%XqF=Vz)>LrbywL=-u_wb$$)Hz-nGe'
            '_^!@$56A&G-'
            '^jRv8|1O+`P>gb8dx@TSiprJYEyZQh+25h#cw*0s8hfVI=Sya^Jz1I%=uy%2XjH2x<PwoJg@dJ*J(&|ad*vaSszu'
            'VmvvIKj&M-f;%Z=W)zh<EgSRTtA_R@d(~OJ+mE$j-'
            'G&&ZA6da1Gp{koP^`2zmu3Jh1n{tE{%=)~b;Y*DxEmno8T^EVhexFjT~IU1$94CkuG!NLp>e9h8`+q8(ZZNqew^?'
            '5biN<jC0|lD}jtdB1h`zRHx3P=b7FMM&#@LXu|uhPEg*?xVkGKWE98Ki=)BHhA>)Ze)-'
            'L`<!5emL69sgjcP{eY86W6X2#*B@-'
            'vdEi}#C?R(N!qvGgA<y(n)C@g|oN|b7M3x~<yafeB(e!;b9pt35b+uK=!dTH*_Xt^lj%*I907CaxQeR#>E>Co@xt'
            'O!&zcQjKWe?_e5?SOS#3KzQYPc$!mUQQ_6F_kJyET4t@`xW0~CCr_8%VkLWWD6h%Ti|1-'
            '5hy(b#|pL^$sfd!PE{WhXRbGB<C%?PCSmgH^-'
            '1x*d|DN=`to42uIGh$sljh^gEiC(@#@b?jN_2$ksHxV%mv+&S^zrW-'
            '?3G)<glFy6*Zgnasvey*H?SVvG`x}6F?4%s5AnB7hv+anAHV5rT;$OjhjhY;>u6OfP(F0(b^p%`ICBnUjMQFAo@H'
            'L5F$8=Kb}{M@^D(M#XpZX&6OLEk4Y)nmc^3UUv@LLfAEzte~ra^B~Tl3XAPku4cdK&PWojBM3Af5{t}$*x~O=UM~'
            '}z5{;(^p9!0R(4W{A-'
            'L0T_Wz>`p=$xT5nS3CB4Jw7lnI8g1z2M766G1!ky`4WdB7&n1nWt<ogRnDf@XO6~hyA(&`CPiS!Wwpgho~1Za-BO'
            '*g-EIOHk)PKebUTG30SIc~g^q0n>1>Z6PmH+S!^d9-o5<4?(=HZ*P|I|u%X&6*nv2H=-'
            '2QXCAG_{(a;RNHF<Fyem-5U+TT{!NM;i3&(M+yNa4qTILszRzi5ZYHrqPZ(X-'
            's@{@d0!1=I}9|;nC|ityUQ6e`AV82HRoCllTA$fBKKESH-#qCYo#-LA0%-'
            'o4zj=lNeZKdqvK%2Y3nw8v}ApbFj1rf3D93>3J_&$jjZnIfoDc`<1K5N{?^yNdvl?e87%@N1VGwNvsUlj%h=*)x^'
            'ZB{{~)LJqHp^<KtMaE!OHtyJ`8On&0;P<kKBs@^c{j02%h9z}cYPn|a&u+>FXT*#UeS&uejeq2yVF=HbC-'
            '924qg3=yn;ZdETJ5}hF3i*NfQ&>`f796R;<gIjtfX-J7Cmy5btSCb}EB7pIyBgLHtud)%D>S-'
            '}kj2^I>q=2$w%$%x5Br+m{sA=^6ZRf*r_pKKLre7hjP!zMkApEV04j`SP;%lJa1N{{dM)tP}3}C+<LLT<V(9cAmy'
            'Z$ZMlg}=wf7|rzkq8bYpP#@G{B;U;r58h?fO=izNb%<<K9UwC1lHTbxUW)R41AJ+3zj|g6D8UzB;F5302)z53jGS'
            '#&0Wz($Gt!-Xw)Vt>npdb{aYvr^?v~ujl>I+?$}~noZ168Y1CNe$FNe5d$<p@J+6-'
            '5fL?fq_W;G7w7Cw5Ey_kx8ySk1jc=CvdbKP}Lxv6{%%3ZKko7AV2kFz%zUizK=%!LGv^*6wu<Qb+_E9Up`1BSd>1'
            'iMnNPjoHRhqbrOWTuTDf;2XHpBwdPm$eu&nly8_wX*!`&A=>1lHwNLUm*~EADegaoP)a(tlS4>_Jqf6s;&iqoIIz'
            'v^t$JcPYc&-'
            '+TLdkTiao<xx#7dE%4gNz(%YkvVVbncx~gfdY#$lXW@5#4r>28+Yj)N5;44cQy&x*qih*;D>RZ(J<Y(XNhU;+i=z'
            'w#yeRS9Wydf&Gm&fM+EO8a^ELH2<KY9)Bw77@;rWP*^>L-U1yhp&y1@1teY-'
            '3)Jf1<bsSceDOm$3N<k$JX6sTBqjqD#0LSDO$xQ8g3*%swjaVA8m{MM@r~~Gn7KL&3PD}{sgwsG0;;mt{jUSQ5&W'
            'IBcDe4+eacCQ)gNnVro=ARLL{2l9k!S%Wu;hZ`kp^cDrwFuwIsq|I-'
            'K|O0qNPbVV&DxDoUlJnceNjy(k`eT9Ls+xd@|ucx>2)4RTuYlO46&Yny2&$mTqgQ`YaL760)14z?$wQzuO&YGx=W'
            'f75r7d6aRX=dpEu;1E6OoHcB3$U72mWGmD#O4oe6HvU4QU&gSrWl&IZvbb;fUDo|Ji+QC=*9f=P}^?5oLHcFUf64'
            'JKq;s2`CCo%O>w-(u}{MSj)E-0CV=zYt!0Y++>Kfl|}g&L0CTn{~c?|ZKF0W9@fnIGdq2&!m~l-'
            '~AjR9C7qI>;xrip0ayk3FA?k2?;@{mNAjGwuGA_Hj3&KA-sn#DcaufIgN9d^{DIM^`4feQLy|G%(Y|SOis7Gsd;-'
            'wXIWXHgt7FSL2acPm*FZ7OJ0{FEmnl+LLZgc|E&eQ^-'
            'e6j@r{F%#F2%O}TQr%X26;iglH`gs}A@j6`lTMTnz0Ns<0n3&961CZ&c=&^8$^@zrTC+t$4-'
            '<}*#hgO%|BXMkdRElxzC9gIy+`A@+9Ej(4t8ssZ}g2g+A>2h(Ic6L#c<FHZsDQ+JRR-lW>m~v1iF-FRC!G+;MizC'
            '&w`j_LT5CO$<S+9&mleBx9>%GrpZE#wwHCXEa;aYIs(4emg0yP57KK%WleN!&uzXcL$+k6v@xoHs;Y^#3O9vsjuG'
            'PH>g-'
            'P^#j_G&>``c3aEjulcCM1}em0z)t1VOu`E58vLaqjjjjf#W8zynV0!EzaVWGhf=>F6(R&7K{3g(TZ`_(eA_bAoB<'
            'SC2gk@8hAh^PgTuui#lSS(|ghi#f0Q!nCr)pdWpT*%LTqG(Yy}UT#zY^+NaUj2b0H*TDBLAM86plVD=<y5mYou{v'
            'uLc(Rm&9lhUho$S1~QxbLfb@%kF)t+8NKE@$P*Ro!wicU6V(sG6%MjoX5M@5OAlP<o}?64<|4wzK%{S24;}NsikO'
            '{`?$jo9IUS8kn}&@jbLW7lEVD-WPEbu`l&4rpZvpD5z*xToGz#^rtM?RmCr;R$Zy<U8cnYrp1qhd_3A&gBYJK9Ry'
            '21nkL{u7-to9J1PsJM~xFZtE8!_I4t{(vFPwH>tH}#F4pu1tq;C5REo7fPip}M-m51RCro9(TT0CKd#fzw@SZH-'
            'y*RT_iH&~@AEpqSu~gcPh|<w^P>R1FL!<-1to310jm~*Fo7m0RrC7-'
            'EN+4*t0=(_hWnI^^(`wnLDLhsUsyO<tXWhMs7Dh6bkifaTP#@DEZw7qjBh*sGs-PHm5n0?sp>^jGvT`W!ii5`)Fr'
            'KM2%%TTcT*{Bo><%Wkzr@<pD>ll7wG*D0t?J%3t9uHfF(EVyMrL=|rasa})tk&k)Qq;BihIut?oW-fZKA5Xtyz7y'
            'V2oCJA5M<B9?Q9~PC}g8t>T?Vl3^m_)g8dVEPij$=Praj%3H5Pi*T_!vP>)S6LZ;WNFe5T4JSLEYw>r%V3)m4RX%'
            'rcx3>0A>C^Yw#0#|%T0nm{wR;N(!P<#B@YrYGHHWY3ETZEBLc66~C_Q-jS5h^2d!}D{vH8?A@;cFvL!DLB%DZTi9'
            'Kh2gGbltN+zJzp$C4GJuK_eNX%pX&k6`(sm{64k3>Msxg|?^Y_XZiA#YLGHHz?Aov<0**6RIcvCYR&hk!Dac94FX'
            'gO9QtDHIylpr2U!2<Qn{XlOs}ag}wVy@ZM@m*QuM!I5}8`Vh8XCA&~H0giKP_7-'
            'K;&mDAiX=(2B5sJ1Ju4#`8ih2wJ|VWx~p_RJc<UdGYks}qbA9a(XsBUURbR=Fr#4@(~w%Wetj4|GGq$FO<Q%a#*!'
            '(e>SPS$-U=q`mUcG)QGAvRIb->^L{j$1&kM<AYIYiY%tR9zN6<lVLW}=#)ClBDB<)q-'
            'ReaD9*L5_Cb6Ww{QQMEVRcfB?JsifVyxIaC|wd&mpU%{@w@y{qD=uuZ=1P=?_4)VAat<Sc$9>S4~%))F|MMO|%l@'
            'PQ|_~q6ybxae1F2INQ)w_+4hN)r9qUGhfQcYq)MREJ{Q4X-'
            '5;Y<Cj0clMR_(z=v*j1L^R~RYec<$B<S(cGvR9*&Pe63L~C}L24R^<rQR9^vW`;UQ98?9Q}TH7Usn9gN3h!#8D!<'
            '<dl}@>9^XSJq3#qJB&V6Q{38FK&0V)7|KlG>N6<91vneAaB&F9cl*iimPT`nzWv6K_q`Y^uCH17K~UDFP3c9E|6p'
            'Q0#I`L}N{mALO?k0tu*O0y?hooN5}XRJKPWyyzbzMWx2?cqKqtr6N0dc0-'
            '+IF#7o8z&?q$7x28l4_8zsp>pDaWnrvLkWjjAEO-e#+1ruv-Gg&a#)G<|H-PTd5a^*-'
            'tdFFC{b#Lm9s4ToEljWLpefL1dT-'
            '1Jb~ZwM8awKC}XS&9BX7ctE*3JL*`LD%8T68Fg;&PzBPVM&|TB;kS*&w&eORUUwD3p#Cx@x78NfJxSB>0b2k#qN1'
            '`+0ZH-'
            '$$g8QSxJPUfW;3T#UI?n!=I^GL_B>;wDwvwU%k7}kFS@SIS36&IXvvP6X$X@qtjalGJB6%xXuLU^%d7c*xAh$h3L'
            'g7O497G4zmNNhjV2Ogs|GvjBUu;w2s35BKaR6-'
            'Gh{A*BD~yUy}m!&k}QmY4m3G1T*@}TwLNRs#;d!3iG5hSMYDfbkQ>)-'
            'rx4JLVb%m*@xg|Ph_FiT$jMvFV;k`UCO^8Whu7PY#1s!YDH%cTz!r$|0v!|2~O>77e8#yc?Clpx@vverKcc>MCW}'
            '+WuIi6#R7<DTa~~{S!8bPh4;dfu_I5I0T8k^nZNG7Rh2ABwXuI|faewcj25VoPrrE_1!V@HDI>tJ5NLkW2o6(M(e'
            'z%UKSI97q`-'
            'PbSXoHvhjolI<`2SzNlIQ&!=l@ud67Um6DPkC@A&3?xJuvtuY;ZcD0cp~yYu^TzH{~fP$Ew;ti)bf27IpAnvg5=o'
            'z$+Tl-}a70zrO@i1FJy#tUc-'
            '+ITs=NFAuKa!a2FE+D)X?`6rQhg3{UJh!4z^Y;e|FD?}X%cA@sUJP|{<#VJ17l)!H<BYUCsp0YDs-_BlT3$y^#e_'
            'quiYCMzK#M{UN-'
            '#~TI7x72F@S+02=Hjjc}c&3rz5tfzoNuXi)~V;2Cl56Kww6}AMzqH0ndm8KBMD~V$Y9Xu;6cgOGESgYH~8ja~M<x'
            'NQke>dHuf31-)M1c<^@q-s94{Q&|f2qcBtgiStZ?M;-wS=~|&|BGf{X+EFa3gQ`cXUXwGi8=U9-'
            '4C1Ny!(tI>w<b=>Vh!B>t2uUW)v9<S$`5GI7!2|^hsUqpoaWCDU;c3Vr~LTf^z`t}OS)9>d{(M*)++s9zcgPC-'
            '#*wm`@`@Ld%sK{!2gbanSPo5;XmQO4>IxLZFzWxP2lf8WU1_mJ?U=#vf14||62U-'
            'SLc&o(z7o!@!S8C4l;Kor?2uKUqIxQJf^+m(RjD~hPaJ%?)*JbAAYAAs1IMs4;%SG{a#I0^&;@8vA!+TFgt3TrT('
            'JVQq3R$?CbIG%!kJQQZ4ZB-|g<|k*mezD)_N%+|R#Ff6Kny$s6E4OlYggaTDS@c&Ou-'
            'z2pSUC_hoSvA}&)2^rE;FN6@Z#*)h=bim4{f(l=X8$*G~P_omEO169PVjVwy#&Y;oji5{_G#&em<+n`h3{pCKpvs'
            '%n{w$C|e#YUjVkGdkLF^n~Y-'
            'TfTGE{S@3rHP<CbG?<qL?+PK6<&TH_PGUpj!m7^8W0Ikr?C$Ls<g8>=HH2HIst8Hc21H*YGIIk}u@|UP%EmG+aP#'
            '#BxZ31dUdBqv>~_YG@XhP(-hSPKn~sISCo+!ey4_AmENkT%c*=@_<UN6nxmKK=es&X;%FKUj>N4qqVsV-'
            '>rp8(9SAiIw9;8pcP2Ene#ey#9HBk2i6g|;P{dV2~Q;30ryY2ZHY28)i}bP%9EAV+Q7Q&^QFuH?cMv4ROL>@12W6'
            ';)-_lxOn~F*;j@DupPwpRKR$SK@ZwP1vi#}clcN_0&-3Hw2Tu-'
            '90=kxGxDccq+U_a|2PQXPfp!nLeavz`Stkc4PmYenG0_68htq(N2S-'
            '^89^tFaDuK&4HQruq&}+U6+FrXMe0fByP47ca1@$w#mg6OIy!ob~O3~mevo4|T9wOteE}Q%4v3JxOKYP-'
            '3i68`HKx_Dy#MP0rLrorab4%lG22qJ0rSFcofAY7z@vS}N-'
            'GvmTz~ggFPPJAgH#r3SXS|Zk_AXF;#dv#cH|B{J=%JWuaao!&C#F9)HwXGJE-'
            '{I@kuIjyWF08cdkjNJNmKh<Hk%1z=wJTw^WLLmJ|88|_a2M?{^c(QC2{WQo-'
            ';16BX<KMRIk>QA9*aOQ?(u<pYwL~?V0$GlsYigx|B7z@2n&=FvMPaYT>4Yt<!^)?qe-'
            'z{Lg~sr+UzP^nK6$p85&z<Y*nUlGmqtFJMHuM?JtOd6ZerMLQH(<z`LAF*yibdiPhES%tK*NVjY~IG)2>XmX~;;A'
            'lg?EBoN2E?1KP%FK)95^!c!T$>aiA(SC|v9HgOv&qA^LpVhT9Kz?~+Ywmw%VNX5parAZ>Z)i^dxSrv;6~k~ZLSV#'
            'twDDm6n^(u0-8ZAfN^Bf(ukSSeLEEM2=-w$t~o@`30Yn4dKO8u0dDPaSyUL32_6ati0!;f>?G-'
            'I+OIk6oUT>1vXh{*Q-emMWQa*VM!2+$zyS`m@FN<_AG@1`*<s$H%!!blNe&wSesq>~-%_Suq(vz2S=&!Z-'
            '9o1=eh#H8CAVsGis7@3?g#PVjEe&nwWpTy+BVgEGb1g!dsmvFqT22E7Nz)Nnk+Zxvucu@=n-Ft?oWZ}8&-'
            '@wuj>_+X;*>^zEhg~OM=mk7!+t^9MDq%+ha8iB40yJ&GsjTj5<_For>D+hz}k*9bUzSnr0mo9lhpPmzz17IbprSO'
            'kiw^t2$Urp9$G_T`s0S3Pv;?Wqr);T+P!-duf%!FZCL-Pf`tr8{z}i)@X8Rk7}#CW&E^lQPw{hbD$?k$W!L}Xlg4'
            'sB((i0(2}yGvJ6Ay2AXoMY|(6F>rTn0>MdkWpk_Yw1C`=|m$^{iO{q=&r9lO%<YZ_<OJJ5W*~90KeC19@Irtq<8l'
            '{B*4Jepwq#W^(0A}<M#L4Ly5+V|<YKVV~`XR_Z=-'
            '059Dq<Togr$OLpF5@vi0LGfhfF@!C}NM{sVbZXvP>?nK_U(M_A1#1rY;+KJ$$v*NWK@j&GQ>2Zq<$NS{nuLa7*KX'
            '{g~lLPc-BjRMytu<$mX_V8a{f%pE3nm`0hqtc8TR)x<V5)YR@c-'
            '9>Z#nIl@IZMd`Wz`Q_iWT8sDx6#mPoONr(W&g>nZkRW}GtS6GlHf11d|l7>QB(YAm$@IDH|&S6N4nq&UJJYmf{N!'
            'fWhLILiK?V$xS~BJAQ;wUM2i$Zoj_J5v6i=ZfsWzp8S@Q?KV8>w>MHBXDWkcfy1>#V@`}n0YgyXT;Yfj2t<i<G3^'
            'T$}oBaGn<)kozie?;nY^a+o(|=gygqDbMXXv>0W|mcw-x`l|+&7Lwu=B)o_)NIm>~$6*68xA`%{rj-'
            '<L<L!VjCI*H=v=7OnNNLd!y>}KI<vob}Z^_)Do;=B`f8?8AL)V<dT(NH+9jdtpaz=-'
            'GjzT%?VCE%<u~6Mtf%R0(lE?KV3?*C~!uy7$a``b3}$`VhUZYXqvqG=>?o?vzb%1BIQITg$ibf28W_@WsqO{rrSK'
            'Dw@`??(%+6{u%qT3E!~JJX(mSwzUL$Pzv-'
            '#ogBc$524JMLCzNVOwlW?Np&iTpSP0Ai#NggAeRlW)I7DZ_hftJyDo(9gr0~bIg!CL3aJHl}iXY~)l;vR=rY~v`3'
            'pVrcXxH`XT}tkje;wD5zm9ulNq>)Eg%J|f1RlK;$E{fjmi%~Ltlr6s5DQbFCTKjcdyA#9?#2L4>(TKWpuTZ>W}ZM'
            't0~w#?4vOQw$hb+B?7BhsB%eqiJh@AdyRPvHBLmVe$MyTUz)g5_WxNY5D?%S^`*S3BN3a+K{2#e<_WODv#06yosu'
            'm5n87H^;gzxx8CC!1#>k%VuSiD=oF1TQZKc*#C){`n$Z)5h-'
            '?Z48OweQ@5@J2r=EDxA~+Fg(Z2=PGrK>l75u_*E*wV4N14$gMYL6@0!hhFI!!#=g~5|Yru(sAWS3-FE8$-'
            'M<p6wHZ7jv5f(1P)(Rmyp$4vmDZ~1-'
            '&83ujMBBYkh9Xbj;5yaKEj4puK#E;JRM1^mTk7TfM?RwQCS_LNNrWn)*4si661#;`lr1ED0pH1LY}X6jeu4u3bGF'
            '^h}5&@y<UC$7S7K!@hs9B%%PDfJd`GbdqGvtETZ7(|vqy{dYaYT}8%|$jS$Gr`{}xHJB;|iZ~Om5kr&xAtw>#LOk'
            'dz&{7djY6m;HWkw&eky{W%w?V|yV19$2oks><PYZEIHXdP46brH10v27~0o;v!Ofm>G^rp`STV_^bAdFU$y-'
            '3ZJ$*nb?W1AP!;53?5DckaGGi*M*ZEXr;4{&28tONokyC7msdwch3p`{Iy7T8v0(G9fFdo)Uz@2~(&(V&ldoR5y8'
            'TCmOtxn71g>fDMzoH^h3zI{d78cSm3v(W*rMxB$QNS;_2$oZ$CxNqPYZUpe%H<0!k`H<iDKgHM&NotA)SY%X<OS='
            'Omix1EoiHMpk_M=WDxoeKE;TAQ9<uJ2kR*jU{1RT*7x%OU1d;td0#8NRGhnY<2GW^83IED--X7F;}P1i1<rig@u)'
            '2RD?dpAiroAIsP`%H@lgFr$ZZ{RHXK6$hkD2(1sQGBW*&&nk(gc`|oLy;XNvw)?MQ3>kb%6&p0{u;P8ddF`acs)o'
            'S-HqFFJ@_Hd8e!G$Xz3FFzmVGfrT7Xdl^f13)+^wKl@l&;J>X-'
            'cl~oeG!3$cB_G430QUldy2X2WVu~)_WN+2Y<^_rWZ)L%YTmgAKT_^MaUm6&$3s03rItux6>sIQ$|Zpx++;A$%3cm'
            'YY#ccLn0-'
            'U20V$jMPH4S!3_XSGSz)ohmczw1mbX;va=My0{Mmlz%m|21O7L32xbWp|bd(X=#63aD?@ouci$br<y3tmf>DGmh@'
            '{;iLKYJ`i@!t|;ppxu2i<(t-2_I6?l1bZ=sp?Urv1E)%GnTy!S1hYIN%ftnEG6dumlBn|#j;cs-OpHvX>-'
            '<6ofzpw%PbFZ#<w^0XXb>Yt&kq`N7h`TUk2PSQAAvpsa$?#pbRq{d135Xs87o)~eyfO=9>ZQ1>5?NSmNx665*#12'
            'q8*LIAYu1C?JNR$FyQtp=p8sf@c<73T&fl)BgGq?Aaj9qu?1QshVd*jW)$bG#5v{r7?f4RcQY4KNy3H|a$42BLCk'
            '@2DWS(*c3~s(|W?R*aa#?a-'
            '0Q&K7bv@755a72aJ`!xCGI^EM+gNt@=R!t92VN45<#s6;S*gF3vSbJ1cBaS=?_f~yIRII_e%uBW!$}ukIWF(@jw+'
            'NR_^h>CimVT@R{C*Q5l40{M+W+wq1L@(PPdK6=FUl6VV_Dwd{)k3&uQ?`Ag>GP^`#f7?DC?fE<8Jk#%jlr$y#pIo'
            '5}TLvWLs|wg@*>*lIF>0i33FNzQ6imKfB;dLegYfm>gpDri<hRGL>1c3rH*mbh_e;HG!;v8#u%hhP}8_^=tb+5eX'
            'K9<&OXbFEj^C4_OSjq3<zNed!-8z>6{<^`NwK?-'
            '5J(0ou?JGRGyH`M@Pz%3WfxK>WSFOq|&Cl3!_fDG|?_whH$kLdK3JRUz1c+p%{$d>_H02YhGhkQc<J%FoHG>#3X{'
            'M3MxTVDy0MA5ruoE$I@L((AwE!zNjM5$t3quPayW`+1tUOPG^urI=%3!;^H9mp99i|UAx)Y``E-'
            'Qm~7QD1xE_tJpFLAMuF4*SPop}|)1@$N&!ZVk^90nIo?JgpC@!!}t?=z(PqYo)lHyxGj>h2nPf=e+<!G!md*!%mT'
            'Xz+~4LA>)L-=!YjEaZQgo=1&sYT%@{jQOhr0mmvG2JHdvcT>`Amz-'
            '7bjo+0)p3)`+PQuZ9`eeET;`rmgCZ#{5X)wnOPIJ{g6XD-Aj8X!&&iw9ALA=oJOfqywY%x-'
            'yK(CF)5?ox{l3u1{Z2ma}>M2EP80e$C!BDUo$dS_s&yS^%CbIokQ>KceW#ystYuY#mTsAg-'
            '$@v3E!8B5?tpV50>>BWql4-'
            '9;MJ!@cGK$lFe>PlkGY`vaRn(aN_J+t(1goj%3_1MX^g@Y@x@**9N$I0;4>azpY6_a_rDznrpeQk1K;6Ry)#csc6'
            'W)TS9pzNO>+g8dVg3`8R{lErskK1k@-r&0Z%f9X6!LgR#F37(jE~sZI-'
            ')bW<8Wh=0hyeB4#|dBg(bGn0^_bB_E63ao80=_Y2x4vP^0^s0yz2BRw^Wnm{y+Wc*+6gizCOz=BAouRkR5Pn?HA|'
            '<1uh{Gz}0##J<j}`8`6%Cxuetz`v&_Si*M%Fe6g9Imn)=VO29NT7z#(fg{j}jc2CSdGSHMQ0(17_ejxgdh@_6L{m'
            'JC`4MeBDDbaxf7_aLU>EyI(?5Zr_H_5P}01WY*uw@nkSkt=kEB-O?j3sIEZ;SJ0`K>r-`42ZQ&qey(`S-'
            'VQQsc6j6ielRYdhd&ci%lc|9+ppZC0Pwm|y9P5QBe~F*9Pj2OkM1LlE>a=OeTK=wMF-'
            '2WCM5e$`I%2zeDZg3GLD6t4Kiqw}xJ$GfT1Kmk=Y7aT=7!<q3!skK;uI~Ph3Et8%9w?~sllirgZz5MCm`O#A~UF*'
            '>Q?e|}Qz1x2uDxcki@=#an8*U*?<x@=TfE+_U{T7r}4JXGit$JdW(&Py>5<HLJ=T7-'
            '2su){=+ut?on_2n2_<mkbZ<5<vffI|hU{dClkQ&4@v1oQ0NQ?I^{Qwy<_mY1ff4y9Pn;=B?k}rgO_2}{MzD@4HIB'
            '@kyk3x+fVOznJ2;pHb*%klqtL2AeS2kZlYxUzJ{lj+;<-'
            ')$ZdSqW1P7C0oh~Ed_Ex#A{N{L2$aC;J~Qy}FJ8Zzjb%F8N-'
            'K*uJ!333!)L5$k@`XUMNyul$QGi8m}$d7EuP~Ru@T!@*JT#<L5nD1<a?;b7z6bV9ZKP8~<tn1|-K>XVjVB{wwXp-'
            'S(o~hyWS9dgd*0=mJ+^J*blZbt|G>-'
            'aYcY%YE*qgzLi}?gfYAp!8b=RwET^dpc*@_4Q+Owgzynvj+_20s?e~G8f4ws^2X@wB>*Pu`kV*9$<fvw^@X6tWtC'
            'duQQlWJOildMRM6!6`@<ea6K03khCC!i*yln*M!npU_;n+qt@e%(}Hw8fA^$`hj!c|#fmxsLJc^%KF;C)FIYF1>y'
            'Obwx+X>k~mk;J@ooj~_Ob>R{g3*G~X9jb8pWCi-'
            'N5!!bWEZfb7Mz>hGO^$GGd@R5$E7e50&@^4T|=4m}a?T}XTV`4093As&mH>5*;wHa!O#jM~c0l3Aq*};5cJCo-'
            '94yuS$QZCaPOD;eTEsjKYLO{B;@c+*1_@=~E_24J==<8kgR|SgUYyV$k^^c?J_<6a83bK~I(jMj23QUdUkjB71X5'
            'Yupi^UXaLA!!Cea)GCD7PcC4yim{>pGdKp@eieEj5}g=^XJS=%2QZRsKFcF9j(Z(hk}eb78MWW-'
            'D|SB%~5Me_@&h!`B!3P=H1KllXh6);Tuc#wYW-USAzoALhmKbS2(p-'
            '~!!}+2qQ7SsKft=H6{{KHhFWxx49$DoA#si}D%{FqEmfOC4>vSo;jY$yamQ#ISUElQ`~pqQiAHMdc)go5{uE$D!k'
            'fOF~jvU0$u-'
            '_Vm^5KyRDdc4h7k#zpRqA3wG=7)#RdboSf*+Hs4j;Y|sz(C_`|8_#J{+$jwY2ArMb@pxDCq5aq}l(NshO~)L!erg'
            '0b`X?=8S_NV{<Wavk3!_e>NL>^?P`H7OE#WrkL4$}M{@r`zV^f9S`_`2sEgo%E{KkM8&f;gpVe44!=7Rs*ti)odn'
            '~OJUFreO96v01K^Ud5Ff!`EF@UH{w%rUtT#4U#^6++Iu$oLPjFab6QZlN1QW~E^md}%GwAp(-'
            '#7Vq8Q74_2^i0cf9Bwd)1yg1?3IK`09H?n3A9`STlTtA_cZ9+jg4&R}94P=VKcS@%R?EQm<TBAtW`v7<YNZl4Cr~'
            'oA>nBZ&x==P(7Ni2o@fD!OWa346w{6LY^Ku3)UR<R3BQllg^<TPxC+hNPvQOnw~DRkSOsrNZV?tn-'
            'y&rP9|9(&}RfwiX)oPresiNBRmWtwV^X{<<1Lp1Y;+D23LD7A>1uA_>V&Tl%dnwOi|ELao?vy)NLjeW`KQ?gb`wz'
            '9S^^5%srY%uuCu|R|vA7FUc8(=(N0EY-U$Jw_Yg%8OTZO*iN`VWy3n-'
            '7wq)lTv(P_K?{QgJeZYCeu#WNVn4p3|up!I@7#6m1g*7TDcTjXdfBWkoZ9P7=Bi+~p1F<EY3O>tn$NkWe_(YQe01'
            'QaD@-UhU0Kqa`f)7?IOkv{b(YoSjKex@WWElKy&9!pzZ5{|Vh-'
            'N!SB<iF!5tc~vaK^&&etFk6intponDHsU{#D{wlMeWx;0Y}H6bb2{qg@54v<^~E<|ee>^W7Jg^q=h1d$C2fwgn)+'
            'qv^BQdN#CD7lI2;rZTks+a#mF9$*FHbgh-Pyq;8c8(21PW~f*K|}98&9fps0faBUxstoOrzyt5y^Lp|x65P*y*+<'
            '?`#I(Sofw9Z(#2a=J=OL&{E-H>R3O7fO{sK&t5jY3;?1B32P)+GExY-'
            'q<l~sMgXvL54(b9nix;5`yWsx==&R*kH0WHD#`|Zw<x2-ZQ-'
            '@#?)HXb#Qy46?Pm$m1<zh<Vx`)NRhh1fgBlAZZdrUtE{k}9swSZujK3oB0bPc4}vFdJVhcz&Pu-'
            's9kPjPu`%~Rq=k%&=~VA+nC|ST9_dKc7T8xx+Jlz|&;NXKbdtY3cySmX#CS~Z?0}on&br=_-'
            'b@VZsW{7iikxn~UTt_OZ+GVZc=hT9q;ER>pQnc}Pftw4t8%v7PcJG`aoH}65c7i3C56$jDo?W1s!XGf76Jj^Ey!a'
            '-?u-r}Kf(^_^tDP%HfI-'
            'h1tcdux?I#NtxA44D>jgxoTZUdR&HtZl;hYIZQWQSA`G7Y3MmJ)A$%xx(tF||lXuzCdSkT~aN+}PIjP?;Ne3Ypxv'
            '@&UHm{k5PH(a`IkT=xH2b1n8TUolw47~7^)s~6(Wo)$XCzRzf4={FkfElziy1_B-pJ5conz!%aiGO&az&ni0A%#i'
            'v(Ow*L{Rmc^;HeU)ym0cExodun`Uf2nBq{X2WkDq-F-'
            ')ur1YA_1(}w(X1CMpHRLj0gThfl2JDOYkCvuvY<31?^)rx=VdnKe;Pu3A^*IOTDHrdnRgF(zB8AH-'
            'o0I*F=dPOEY4T2(kjtbIP~Qzp$+WuQOGoRE$(Nuia$rGvfW&52G(5K?ls0Q|;Fl&K(aN^~f!=!tVP~=`PE%{c&sR'
            'H7iG-'
            '}mIhL%b4D~g}pEi?BmkEX#v`{0eYTX2EH3#Qn%VH5n>vH~+RhWxo0{coO;@Af$pyqx2(;w>(o{8r<SmfE?FX$N+O'
            '}U9@RbL8JX}lqiH_g=_sUkZw{=glh-'
            'G#rxzSu86IqT9E3hw@a!BE%blBb5m?<yQn*5?&y(@<VKWhp#Ts63Q#%DA6^ptd<=Ld$b3LLR8oOBGj^Sj|qi^($O'
            's33Gj+ERSxx3EcY|(uGHxAOcdYL7606XUtCn?a|E)TkERpv7xbPs{^Oa;sk~u22ke=qjXXh3&=R7GcWd8C3`{HCl'
            '5rR*-^@RULo=PY>KK6Wjq6&wJ{6p(@y@+|NeiC&2P+Ye%7$!#6TDF=+W-'
            '(DEUSi{=ze3HG084f~aAC8H*j^zr)=R*6USu4t21xCtL#kY5em+{<MUU##f6ckW^3EudI<~ctJqNVy+8etP@x+V8'
            '5BDkXE|hf$H%m$R1$@f@@&*5h=-'
            'Q(8NhHj|!bxR1i&xW4=U`T5Q=E!;3L|>O{Hqi&4rCK*7WjLczI9!MLrInJ_Tml@I`DAOwPUV}1Q?@=P#*Sh12qlO'
            'Zs{;s+J`ApQT#={PhjE{c10QtQU^US+w$WW-'
            '2lxR*SI7*;Zt?3BPl@z`x(6|ZER00Xaj<^=y2+`OhG7}Jeff@?&&1amJo<F<Su91#$KrM6>e+eQs)0c%f~IplpEG'
            '}K0|Nj=-lff;-(*jo~JEwY^XdAG<bTX%GadLXM=*~G@5(D@Rhan5YsH^1Ln1}*TXYRCf4N6GIZd(9$)p><Hm2Y-'
            'W#ShGK&0v~T=z`*gA)Dhr~t5_uQ?=PLHM(iOF|28<Bp0yx@y&}4e;&A^c<NO0!A(sUid!6K$H}!S1{mh_f-fC9VO'
            'rMBXb5`nay{A1C68|YxR&0j;B<yEF#(Cq`z0{bE>u>=drbB#hoy&sZvGw)Hi0jPPz)fNh&P8b@|LjVfxtCa(YkTC'
            'PRR4G9XA&=GvnKd<E4eSIDvRm7b$j2*FVf}9p$!R4=S<O&#{D)+O~z9z)v3Ig;h_b=UMuIUG}7c`QY;q0rCDJ!<8'
            'equdlsw^L1bn`RbH&KN7zQHn^#n?(Pfv1CJS<?2inI42X<O5TUy!(jKd;&s+D39hCvMHiBWojZJX0tn`)z%WU^VU'
            'M2jb4w@*l1A5ZGV0;~v<kyJNX1>JSLOJ;0mm7r2y)rhZ5$_cFu^=b7+U=>O&=>DW-m|=P>e-'
            '1H<Simye?WOoB)CH6nxlRfb?rSkfp+N+b6X~j$p-'
            '?YG@4T4JB7L90@5#Yz7UqdjBi_+dT;AiS&!YQgFK)}u*$WmJ$giOq9*XgD{*sVeifv|wRYe!m<PC9KX*bf0CxU@}'
            '=V7yI)s8xm&I|9-MiD47g4MJYjUod;1K`_xAX8)n-K-'
            '0xy87o>40SoZ=#5+6h=U;Uv!TR>>Eb0~h}d^tSx%Y_qqf+V^N%5J7-'
            'ZO@FW#^>!WTAvTtFYpEvjWFWSU1HU@f?;X4QlV%WYv95>pA3i6hjtiZL$gw(jAXYaNg;(2VWrTN0#n)&tsgLcD*k'
            ')!66Xx*#HzWV=E3XG8_qF`DY-'
            '56KcTV#&ph5UvxYv_zNiuBAloLhG8IvXj%{_5!J<n0D&7jbwO8x#Crp{x)>l2vM@Yp#N$^MM|VV+`WzH<!ar?A=S'
            '4h=$fGONJ(r^Jpjl7$O5*(eQXv@J$p}byNux6!4Pu|9+K6YcbF)lbz{H*$|t7^WpfTaETeEM_IgBGgsyv}skuv$1'
            '}?3SG_ww>ZCM_AMjFSEz;DjUqGMbSS40BVkg<`}GaJO3ovc?SRIYgxV@D->srrOiW*KpARB&0e&9>SZ-ZwNgl-gJ'
            'UFhim6!#IC`KC371PO8g=kYoevu!ILG`44xqUZY9jIHC*BS2U8Xl^0Nvn&zR`aRii_f{&6e7X()BHmusWblPvlz@'
            'V}w&jvk`qgx{xjqSG5vQ$uO<#$&O%|qXv!b}?JCMjZgX;BvocbGpGlXsU?5mh@8P5!<7X7YR2i3sCNW4;)DhP}9$'
            'Os9|iVYeUW;`fu^rEzr|7g3pn+T%>93DrQ;=_15|x>(tIx3mE%miXN$XO*pGzdI$p1v6%V^$DX+J>>i4p|)w%^$<'
            'JOA+b9B?`UFjnWS*L+z0p8j_EWpW<HsrKnzE-'
            '#Y(7bcY{5Bal~JklHWA}!V<jhU@HhE$VmI?cB1Z$rd|TGL{M1KIq*am;7p_@#&k_pEK#P%z)Rj|9B$se@X$3b@&7'
            '{JrWDcc=@kWPaHQ%1<{rtu_8_|l4A&F%(ZqV&10YPt;xy6QUi92B?9t9tcgHaz42t_4Y$rxu$fP8GsS!8H;oYY~t'
            'nl;I_kHNN@j$MOI~Ha0X-'
            '#}$dx}{JqnQ2u*7SAF(^7f`_Q<AH@&{nRyw{(1`rdK_ZGGxkw=7iM#k>Rdd*}>9%o!UDnY0M!rNX1d-'
            'Zpa?4{z1e1(2)H3x`p2t)0Z5&`^N{z24X$2h!)ayJwoO2`chqOK6MlQHfC~w=)CCnP2`4v!sl?v?%OOhm1XU`?r?'
            '0=PvDO?`fAr!t_O4=BxS|%po$<IY%?w>zQ6|L0)Nj&D}4Hkni*p8UQ^7_AqmL!0#p2SCz85l_+%g(3<;Og%1zWHy'
            '@In$q&H+A0!d?_s(>AQ6r1PNR6Vcxp{dTDtHlQ*xCY>jE|+K9BGm(P)kv!sB!@zDvO1u;OGj~4C>0k{3=bP7HLX$'
            'JM`p{jsn?|?>N|84&8{9zSw9}HYGy3WPSn;pKD8`l+I9g(^-'
            '9)gJx4;ERh5!m#`&xno6wR8ES_xVu;1|cGW+>k7T@esB;fjGb<0M7jYlPE9OxaW=eu%sQ=q6$cHyS2SI}V;*Tth9'
            '=}H2(vIypz?^Ay#rZ7WDSWMZmb|fMHV%{H>tY2a<MvJYi0G@0bvgioTB0tMTVOHm80eJic(qns#d@eDu_|}I^6yG'
            'p2fax3YNT$IC7DxazW2)_Tv4w33=GTE7f8)@1tq2J;D|<V3l!aY$z6MM036v}xb{%Ly+yC=JzP3n7V}5Bz$n6q|0'
            'y8zr@omw0f%*SiK&yJLHpz!DC?|}T(+*YI%ODH5xRtre5dY_E_mTGLt(h}N~dcbVx@DCJFenb16<K}opv4HMEyBH'
            'VoBp;W#t`Oq$vrTPVeK-'
            'E15#31>_!YDtc)s!5f>8=}u9l(WcClWZ!?x2KTs`7iiS?Qy$$aK5<VPmS`%8X)U+%BBj;r-'
            '&#od_P5qre|z?u)m?A>1g}kgPwH>ZhL_RP7E-'
            'nQ7D5p|D7@k=2c;ucT&Uj4E_Z3xpGokd5IY>zT?M`4y%W;YyQ1JI$<-'
            '$kvenmmHsy`rPu8HH65p_XmN;uKTam^#cmJ&<ZpqF@py*mmp!H7j$Xyk1zMphO9-q9$`X2b}vn-'
            '6QkrK{HKnjZ8QEcT|>pYBG?1oLpL{a^FFPquDRM7Oq#TC&#^v9gLtQM5w6moS8w&N^=)pVuexvNKCeKO-TBL$d@C'
            'OJXI6vGmeX~i>N*^UE!(jpLb3j=n$qClSy{EiOP3O<e{8t7BTMg1Qn8nAeME0Z<YsWG_CPiK8^5Pu5k@#6%<e!}5'
            'af?@Vg%8$njBiU@IDLq0zyNU2RcjU1|$R$8puUtAi0QXKBa{LqO{GgJ?J-'
            '1xeun(VK_u2J6x9q+wTyMd><z5@sZ{|c4wG!7})~UGs-0Oly1&^SD**6-oz3gmjLF#K-'
            '?;%)dfx?j^B!z2Vcu03FX(Gnrc5driiQUuSP#A~y3~mQqW9y=@zUsOckg1qmo;%Nh%;trZRN2P+1nF=ek=3URA9;'
            '6(-)C0>WNa%SFr{knIHt$=X}7a(=5n=Ju;vtr8yQS{*>;Rd>?Y(E7$t`N6pVvRk!s?pv7)%ZJ@|sr`h$M-'
            '0<ED*G>36Q$(94RU1rGe(n$hW19l)QjrW++cn7A3Trbe2NrqpJ!LvFYbtfycAhXwp>_94NSr7{nPY<mTvT^xgSuC'
            'bd@@1G&?l~{xAb0@CLB?2_^TT*jH06bm2!~nnoBbq(<);BVtC?C4fX7dx45?q%iBPJui&SwJ?td!eV)Snt^zz*={'
            '|muBDS|No6DCCwE!>*utLj5}-'
            'Met^?<^U6^}Q@1IZ*v8gc4q}&ngwWl3ABr)><5km6x&%l%athKpmT37Ix@3SY}WT2HWcvj9(zn=CoR28U#2<G^-'
            'l8It>^ec1w76*YW(F_&0<@gL-'
            '`*&7PD@Kd;~I2fTj&Vf?v_tKdF3n2b+vC5;EJ62o%e<G?g<5X7qLef!lj_9S;3D9e23sGfADI+cARP^`f&bWUJjV'
            'i{n0^qAIJwAu|c$}a?(Y*ru*rm4fBQxX^qp|cXg48s`~Ky?gmHZ(B))fJ@?39wC{fcQ5H{1QmU30Kb}BH5_NQ<??'
            '$>n0vay?2%(QPQsNE!jiZpYc&%R13%){dBV;a<}U{sL3;wiSCDig4&twXzK$isMgWT5EP2eqMQyR5zOb}s=W()Aj'
            '>q`<~mpf=mXXcvw4i7h&w-CXpEDBqL;$aj|hsDogdzEFxu`-KD_QSz}Y_eTiI@~WXO<D^9c-}pq0(-'
            '0^R#!uY$=r4+CwLzWrYZJO5Ga{B3vV_v3u$>;br;<*C9ITN?JaD67(>qN^<0E7cy6cSABy?gRBOiJd7OqI;HmyT6'
            ';>@r}j~^45pQ9phuh%f)4%gNu5(Y^m@37j=rcrw+8QA4j*2^jz@fEArz2PNvg`L;5WcAqXf~x7`1y*1m49fyHCLh'
            'nn>tpeFC7aJ-k|G3_zT{oUHNa4(Cr%fBrRTE1-a?fMLWwkc=d!`RY^&13u8&g(e*xQ;&VphmWvmEu-ON!vD@@>p{'
            'y2J=4K0tJXz+2F{w;BbOW_Je&Vt5pYCypUndM&s=<GJ!i2djKuC2s&tCIoKEscHO1D<QpS@1Pjrs|MR7iI9A~X_b'
            'EI++6X<E_HDn~h*Qq~u;YC=aqZeM<$u>h(@wqQk1fwlpIg7*MF2=jHPtou`Ki;hm-ZzcZg~w^3alsd?=!ezj=5K*'
            '0yP!}dw=4nWv(ClWC6_fpe`J3vJ%pC&TD~{xp+m^H<t2d*g~~kiQX0IwPJ2Dl{3f*TosV>ch-XzP#1w8@izk$Y>;'
            'ySn>NXHxiZB4Tjb|(HLfZq=05`3F$t&0twP6-ARyz>5P}|TCLmW`Y-'
            'Y0?^Z3BRNuN!*frZ=*?}`JdUS#uAsIokz11&TGjEdfH8|ymskf6ZF+7v2txb&Z<1RJ^}-'
            'F(x;Snw31NFXQYd#H|EsWc)x9H?WME{&|kAl3a{e}H6Jin7RMyYE%#>kZRUq%~$;i0dJ38%$?`lBT8pTU*2tuhq7'
            'nwiuPte_C%0U)u{=!D7xBl2-)0e4^^I^u7J})e2AQ`EphwP{J-'
            '5Pvk8`trI`h?9SO2Udv&V#n@%B!HDL{)5l7=w#g!w^a8AW00)Jv2sA_DLm&!|^x)H2Qo5}u?Ka51tWC#pA^L#>o+'
            'Qdt;)jO&7OGN+#Z<+N7h6Gqx6(p0X9te;Hit!w#}?0u3zSbl0K3hiMy<Xpwn;r?yOfc2pTUIb*}r^9+{+^77>~QF'
            '!g;@V_~)*b4Y{|49`Ylta`(_0Y!&v_9`feXZHa~bEOcE~y12j}qRam>7Pbfx`hh}F#Bq!$z8?Q&Tj4^rgn~AVZ4h'
            '1~JzD~0w3DmoKW+9241iG%=Oe9tPPGAyME_?n`~jI1T*?Xpad^)1&t}fs#x%z;!gb?x(+1qzmgb4__cEcW2(GDie'
            '~E;XYkE;%$4c1AfI_6dv1?@Bi3qdqM&%Lt?!$FPX51UZ6-av1RyMS-MxklS)jE(^V-'
            'VHe@rXw17b7_O6ykO?Ie*Lh*+aJ$v_)#Gqr_3PHik`woe%S;vo36J{kxa7p|91U+hVw#Mtn=7VOUeHi3;et(;fqC'
            'sSoeB@q6SD*wPH+nPc?E!)BEA)vDfHUiAWrvZ$bM`}fkbCBbsD!28d|i{52j>4zKrtu5^jQCx+5PssXE)hvsoOK_'
            ';9cKfzx&V)1sN1ca32)p&Ws7|vTl-'
            'q$Z4#M7+oo%f<j)jMwly;&*wjO#jS{o{ZkNj_Y<1I}pSr0+tlh{Xsx{aPjk$-'
            'KQ2xm{itVvkG`(L({|FWfg0$U0}>K|%GL3>H$g#OEn@~>+~xwjeQ|60<ed8mH$D{?0cKt31!+S&m0cOqGyj#LA*r'
            ')BHb9Mt`-'
            'R@<Owf7JXqv<xZ#qv&|wSF|17wm>zBX6+`kHlx)?84mkf3za^O%E=Q4zpY)+Lb<=M9S)Vw|I}tUlK{*!y2Yk+Y;3'
            'YTXkN?8qNXr%YqlKiw64p8_fIFlsvCQb%3C<YNA+d@w`T;2+rYFJJkTIHUc?Wc4gr+uZLYB}j=~HchTqQ{{-'
            'f=KUHkp{;LXdUmp|+=m6gnO*#dyJ{d&L&0-'
            'z&vV~+?(H#efXg(f+(N_3cuckSL;5<f>`#6D>uoQ#RtHonX08$}*8+)2`s+uRA2K3+uAMVT|RlLbmcNHpl@K8XVF'
            '&9JLXKLLD}m|=k7Z{MJ!L)%fog9j;nCrbGDUUIOwX-'
            'kdK_9Qr4gz?731a_#rYh|85G;ylONtaWHMgvN&f#sLbp8zT{RH{WYEDU80Ej3LQhLB;HN-qKk>s6wMQDkm{oH$yM'
            'lLb&ec}2!z7+SAh!W3=fV7>x_y+O{)QXD!+d}dvvBtLq2a(wvY^wpdE&EXG6C#P@zoFAN?zB&5ikEe&D<n0*&ivE'
            '{kDrp)FoOGr%XW$VF)znkg^~A0g%#x5Z%VFY`0wYH)WU|?-'
            '=MoBeu+3F{4TM0jOO1b+qlESxIobaKY$DKHbCAWX!diD)Nxl?#C>9K9-'
            '}x(?)aO7R%)ze8OVJGF3Ovwzo?~VWrnK6$3;M0O$G~bld1;6fL*a!+9)6h@tIN$CU>m!z(s{{4*pEe8o0JKTjFtq'
            'LE2rEGRhSsl1}xARy0ZOp<gf}tl-gt}uKudNVHGSbuw}e0VB*mFvMMS;bnI`)B?wYaJ`@^{L0TV*BY3};s6y&*#n'
            'fkZDtG5p^pT05foh7$^d}sQX8v^zo^9(23v(00E{LsoYc`_8uM9?Vr8(Z>Ty$e4LWX7(*(y#_P17+OT|)K?`M%cI'
            'i-z+}^1VeW3!lH*c}fhFSmiW1zoF_sdY18kBxfq82<!k2uZG#Dj|A`Xn7$I!q$&-7Ho2-'
            '{6YA4Y^EMieWA&T9e6U;StW|Qxi}OVOI?x8Bh79MxRT*YWl@kY%hdR*USpFLv4Xy=|&7HE~O1j0C9_t0Y7R6HF;5'
            'xw7nSD`(aRQY<>5J+T6i3?i3k7DmrtxAkKQC9WE{@fBM^f;Ri-'
            '5u{?hwC;<o*wEVCIoHzFA+@3xZPvv{fv3x|w(x%v>>F3HYPr`U=uz5@Hb#)g-s>;_k-Ic;aP83<GqdTB@2Mm$eNR'
            '_UpiyuuP$wwXcixm7v$*#|__QjeNJ3MprO+du(y>jpBDY#5=+h!=ZtyBV~Mm^}0)<stJHzmU;mO9-'
            'BTIgxG#Nc}}o+Tc~iGpHkf(NZ&VynI8q-'
            '2<OoclN<H)XM+&`(!vAv6^`O^Q0Bw3Q`Tvbb4GFKv@>XGCs9Ui5EpT6u81s6kTbUy_^oMlKuQSd*))-'
            '|Ts_F#rWHCE&}fz$Rleb)Dqc-NeR8CXc@7%dG|%A;&2yOp3m?>M@c#oUFbTT'
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
