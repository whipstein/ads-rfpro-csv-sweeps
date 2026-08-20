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
        'bda55a58cfce2753e96d3106ce50bbb455b1cfe6eee0dbd0a2805fa7bb4fd5da',
        (
            'c-rl~?RFbSk|6pYPf=aIXB%aK5T&-g(~#-8v_!diRv(l|+uI{^s*6B@tQLTRQGh5mhv)1=+-'
            'KMa+b7wKkNnOo6ezj7=bq_%cPth%BQql-BjYP0(lk9@tjkp~URNK=*-'
            'f%sl^?3|I=L+CdAVNQB*kKqG{uK<lDsUNtA{7`YTYEwby+TxRoQH2;;(9vynTMMs)xPa+sz_bUsa;TcvUUe;-'
            '{vXl;TsF)XS3Fi9zbWmgDs>IbJ8_$E6se!6r>P6Q9dTuUHhbo2F`h-'
            'z19yW|sWrFUw+8h$)q;)AH9%xfqwtU;Z*kisf=vl}%DF%4Atri*-'
            '_n|36t*b1`ZSP<ymCIp_dav?`}!_E(}K&Pa@-'
            '77WWDCeQ0t($q6p_qbk6s&!Q_#7ft_aj{5>SyLyox|kp=u>ye<1;|4dp^4$Xs*|RgZ)ODo>=mmr8L!GhEP9ZLWo_'
            'WU6M+W&Am&hu6|AnSrcCDbq?%UcL}2+0(7CEED}g4tu04gHWLmFageC##V)S*r5;MBKDi?@lu_sH>p<eaIv$`ppV'
            'FK`Y!^GItg`kHu5W}Pv2wK!@Tod+{JJ(CowAY)i>Uomq)6IIbD)T(4=7@=6A^PwFd-'
            'B`rQcSQZ<=<E9`Aq)15|dun^{kN}=EeF-'
            '{<~IRSE_TfxeyZ(6rg@<Zqz?v>uF|_VqJ^{9>f~u)YK<xu@nP|^~zsQU|jrReY30<m-'
            '74J;$|RdRiNc!Rt}Pvg6PDrgG5qduh;t`ITA!dw2zpU<Nzn)lyEz)=W`&KF(OC|-oO@JZsz4;-3)urj-DU>_~I--'
            'e0BKZ&!@+y`K!a1N6A4VFfD)jx7V*<=4Y?-'
            'qyKq!^y=(X{P<kZVkt&{wV8`;OX_Jd5p*G_u9yNTz@AOYaWw}*!Q&x_BRP5Y+@SYjwkh!tZ{~UuZ;wu1zdg%O4&R'
            'DNoE^Q*pB+6tetGyJKY4NZ^aw`&LoYvmb$W92^z8Lp(fo(w)3djK&JWMd-'
            'X4Gd;~7poUroh6<;X2^Ibg2nuMs5F`+wDz^abYsRxS?CR+}>G;iu#jy8Z++9Q6|MKS6e{#Yrz=(r{=bdmx5{OTjY'
            '<7}zxBYHwPMVIx<iU~G-'
            'RGm_;HsTbg>Lz6GWe@98PUg39yG=h!CKPOeQoE10pd#5>{0J7~lBcl^j)(2G(#6`8hDJ4jDz{TW>n6`|$0!V?qN%'
            '?Ukwrh<aWi$7?0owhEHhh$<H_KW1PGfkG42Q$>t;>6}79<UaOt0<&ctV4SpH#)=qHfmJxJllZg6NAGtOlqKXi-'
            'dS3CxWz0&yp-oE<@iKE{t4|H~V=M)GMj6Ptpk6u-_kf(061lm8I>by2!-'
            '^6R3>nahrn3&ClyMY;G;t?C7wK5QX5B{$iIhaZ@p-<H55PKryLM3Ex*=*+FKiP-'
            'o{O`Y`;rY4RhT_1uj2qogEUb>q;GH6O}Va4+_*E|;-5$2)D7=h)$<$MH<izTw{a<!^g*oAlvQk6I-'
            'n<k$X7v;?OX&Xx5(!)FNEnayxKJZ$kHS&!pQ6Wy(xc*SC>}wN7(s<C9W)3Tt3p760oAq+DHfTm3Gezq3e?`{;^gm'
            '~MXT)9Q@5MQx#o8#nicr{QQG6(>8Qckic8UfFc6U@AFFptYtXDS*Tc^cT-'
            '1c<GBp2mcZ2ba+kZE<f0UQypL&9hb@ytYRW1J@zr9Av_%lzUdXCgDPBt8t>{j@MvHI0~Gu9#9a);t9}drc9Q9ola'
            'e;{G3Bm6M#NC^lTR#LZJJ4QAsvpcdtn7n%zeM5FhGm^mGI>@-'
            'XEzH?X1+f7>o{{ucIuJ1`DHkWzsK$5e#K>_m6L#*nJM{?={NDdCH$ym*4r^G>B@Gw2+E0UvHt4WbK3tTKNt>f;F+'
            'ySsh-<nk4n66xYX0-'
            'r31sX+h<f4dvAF9)rR3wPPYFU8S4dCFK4HU3U97DiLE_f^|7WuF1TwLU9kdSk_KKh6pK{m8-'
            'F}9E;hqBR7a6*Bh>uP<~PiNI)^D)gl42d5ue*HMU7&dhp0s<SHURR4hJWl<-'
            'zlt9w^>s6x%x3Z4lR_u~i!?m+xE|NVaB?I5O%PTEC=7f}9|3>wPtzY4&1T70%^PtUG5Aq(YmRo8Dx}ToG0<oLW!`'
            'm+ID~&FCU)4ohf$CYuv4<C>vb~#DFA4oSdFhxB4F+8@Y(6ZqnF6Rpq=JlC>NdFoQeUz8NOLR6*sgL%iq8shx(o$B'
            'yV0+7pr1*bG(?=JyS*i=}s`_c0ypDvO?js0`@ekn)N$a*SYBY&fqD<WRlC4H+_A<A|h;-'
            'v6ie|ZyhU^2dIAxNiYOywVw_7$G$#J<;O9|QLj&NBVABH1wH%V5O6pQ0_)~-'
            'tgglnLvh!Xi%DPh&FpnD3SnQ`SL!1rGpB}&#f|u#plFHxCbj3~14$m5t$A{|e=x5G#T$W3bMJ@nt#5tdf5X&=C)D'
            '#q%}~tF0cfwvL;>{bJFPRG6_ERk2BK++9dN01IMXv}`UW=<lQ8@GXz^xYHkVW2vk8rW!1PHKI9Zj<X&odRT@cr}u'
            '++u-){bx1X<L7VAye>1dJtIZr*F>kHz$XnU!FaG{r08!$B#c8zY-eg*`Lxu0zaEyGW$*zpoA(b;MC2K!4EIXb>AI'
            'I07|o=Q0A(2Uo-{8HRUq%u4shk-^9UPz_um@C<H|hprN^lP15Zjn*7Q-'
            'JG#SA$a3)Ceiq^dW=oz?F`Hc!<M%k@2Kbn<Z38^ZeY^oy<+S>kkz`eVEXSKQ2oj=$YNEfoj0%=rfK5&;16HkDGTA'
            'j2oy(@k4u-S(8h9UGbZ7^1Sc1I*$*mL&8o-u6E`&h-'
            '9=}{IOEJ?aP_0;sLmug$PL7UFUq8>E9luQ#D=@kkR2G~BqQ+>S5s-'
            '2Yc8{wXFCBMGam~Gb{ioM2kMxMTeWw9+b4hk|p@PT^js1&D?hzhUu|GEO4wsc=DDa<8xv_*Evle2MMci;zS>phS3'
            'uFqCfGJxus21*8+rit7-J1@-X7SYn%1{}BaqTItE@$;c-'
            '#D(B&o0E;uy^dpI!71V?uJFu<gd!{dz2?Y{gHR3IW>~Q_(C!`(z)4RZ0j13Gfl<sn^hykG9etoV((Imcx;@q*i^2'
            'C<^k*_{beB}z~NtoSl?&J8EQQ|%W@`U)3m>+$%-LmL4p;PU-hv_4dGSFmbb=Yf490zt_#uzru9as2E}Gw3*3tPcQ'
            '(5j{<267U@TdRg&J4o-7kw%UgHQ>bIYr{GyA4s*(Ixa^N=-Bkd}wbn*{U)ly1w9LcW!j9dNV=E-U`;kiaNW8!-'
            'XGHmVp(%y#Wtj?BeJXIFit=aD)qX9tF1eYn~zY^CpAI-5*VG@Y0;%gzTjX~H%ipjq1af$dFXhd^V9-C!-~&-'
            'u*U)H(@?*xS-R5<z|EX}y_AF&GWbr1e<zf}1V&9^nbqhqMj+i%k)Ru>MYsClFf-OpC2IxE{%V3zBA7J#E$#vE1ZA'
            'qW>1aSpb2?P2UocQ$@5XfPohH^SRt_Jt4jN@X^yPvo<{0>@IyH&y0nkL2|JH7X9m{0s|C@o#1r?2NRoj?1PeeIyl'
            '*1^Lmx9$_*S8!$3<qxNlf~3oYsN?A6x`R9w+3M!@*=sh{ZB72<QfEWt!ToKEYK7ST(e4>16f(2npwV3hAfY8DD5L'
            'lG=mlHY|?SOtqsTn8yladxAes7dN<iC8YK3oNA<Vryn%X(u=9D=|HTqYQAUTU$yKtZ-=Tgh|~Y-'
            'TLQhA_NrWD|=%oEj`x^FU3OHJIAki?#ctkE`yF{>OtaIu0e?FD>2AyY}j)=tB0bLeqn0=#`Ff*aX{{|K|+?-o-'
            'cZLGjh-bw{vM8VkaAt^m*sn-'
            's4G(j%t*W7Q<q*f^=1Y)P#;I0RwykeHYNP<5L0T&nXI4?vFno{`tk>t7o}tl(|BhIRYA<y}7g1;Wn+OQ$gWnxq!*'
            'es|9!<(>q7D+;W!iJiV$Do)FC0nIlk%GI=5gzFZZ{E4b-7B*8gO2=Ya-SqO;(slPCKG~(V9g!IHdpwb5}ppVN$tq'
            'c6|<<N%C`~N{OM^>F$wOVWpo~NdS%U5-?)L0@~h{~upjZYi06YZ7$@tynu6aeSSwlpS-'
            'C&o`}|J^xjdJuFlyRp<cUW2{6k-4a)fL5#iZCH0nKGcYXzhjVx%X+C$Kxdx!K!rUVB$}vVxI+uPF)z6%I2E-'
            'mOxw=ZWW603ld%!Rm<DRH@~%`q8<1z4J_lW(>jrO1)b7BAH8KZB;a`jU(y}5$HVA0h3<+p<&Vz{!o#b*vYpg+{oZ'
            '>jF_(TID1cBM`JTp@`#a~*l&-6@NfvxZ$)N%@OO9()Tn!Q$<adH-mf)(>FIpgZF(bXMcHq-'
            'QwSCrgJRYINr@}t1|FgaB0MowuI;4u#p;Cm#A;Z!n*QMgtcXOrG}yM}%g+Fm6M&PoX#DEQH6E7bk-UOOhzQ$hCOK'
            'ory<n<m-'
            'YliR)x84)BXt!I2ygUS@4JrFm=xe&L@r%|B|2bN)=?b{IAf+xbAP}WI=I$j7}=UG+E>Pu;;p(}GBNFJn2<WOca;7'
            'rHsa<2CTB^g8Q#4~~c0V)O|IhHXssnJpr^T_y!>(+nn>wg+5n{|TaJlhYkIykgIxIjP&AA^856C$fTx9unf4kj^_'
            'ncDHD%t1Zu>$n`-ZHLMNLM|Y90Vq-mDxjw=F4;nvkdLYS2;o3**#kW+HuG{-jVUn3@H|l%o!B3-'
            'CB<4y?E{6$r2I=NZye><o#A2V^Y2-'
            '!T@7ao3+C4S%(I{=Ma1q4$FS!B!KrC~r;Lx{*eeS8>Ej>HH6s4tYlH*A^m4JeSgwksK#tM4%a#FTA%R^7Y8~KkG|'
            '$G8ELEEzhSaaLDPnGUbfV(#llHl)Ez)p|T`~bnoLN(?8l|+*&q%UiL;O2xalQ=~K!H-'
            'Y+7Tn>X!1Ij0(xxc2L^N%z=%{35-'
            'r4GI9Zj`a+P5G+zKoqD!f!hlwLqQhd5&p$^^ld;@cd;W9Apt<wnR<vm1S?e$x%~ju|5ZaUR^%_LF9Iw;~H{T2ReG'
            '<iPi|!n%7`yJVw)8I&`trp8=?C(W9!#xN3^`ksYm=Jvt~+Eb3t)?>~jd{QJP8k=q4=e=Ees~Je@CeK5z!!~97BLu'
            'pv*MbNehrj8_IZe_>2t`0I#ntJ=TY^!grdVecr^&Habn{+Uvstp*7$J*%QKH5zXED^_>M(($1rV)?$j~LKXrE%dF'
            'ajCF<FK;|qLeqJl6;2JyGj!sc`LV_Kz7XNz+8G#;$<jM9$JaSwQ0UUE+e)^sQ4K1&4U}!Sn8S?Xzp@uOo_yzlC1Z'
            'lzZe+XfZ{5&G~2>T!Efk<pvl;z$#EWy<SBacuTW-'
            'l$X{wG0s3}D<Y_9GpWNCA6mssPJFty_e6d*oJR`_g3O=r$f=f_~-'
            'adZNakOnxt8!Tuf^sz}OTA|3>n!#>_2h=dWI~FE)xf;YS_O_E)+1NkXIuIpu;u}75;>kWph|8*fyw<_u2thkbx`P'
            '@4e5UDQz(M!Hqb*!hpy@0@s3!FFOXa?HAPqAadVF&$^fA=D2)c;i6OymnF)<6SLtE*U2r2A87y0?@!sKHo@e3B$0'
            '!42Uiz+3oGY>&+L7Ye>r`N;8#6z!BJ`~>)SH!|P+lgR@w)#dFF$i`OLY|o0x98tIsm_KzeYGP5OZLo=Yap~FHmoy'
            '-2-NCET$Kydb&fRo2YM<@VPXiJ`X^MAaL0r*w{X}2hPP5?BZ?Gfxm6Rj<gR4EVpkt`k8gJ^R>FwisfC*mI-'
            'TV-|iC8wqi^lS=tfpmh0T6il#3wdHEp8yy#oZgAID1`nROz+CX)@E?Nvp+_5Av{5B-y-AO&OSrp6Wsy3%6m4kpG('
            'VQ~O4(B?l#%slwc)~hzAMM3t!_ptgucRzb2ZH~H4WFuqG<n`JKG=>U#bd)Z#m-C+AqZU{fv65*#(H3-'
            'l1K+=uiFKdlIg}+q~S#+dy)|stI(KQ<}_}eIi7Of>RYmy83>Rz1|Lgmad*=Ayj;%YHMi8~+}_WNLeP4(DAj(CoSh'
            's5UamOd3uv<eGrLgfh}2D_2q9b!!a>70F?=FrocO>~t`@4%+))~L1O~jd3<YzaTcMc-CdGuG8^~0UbR3)^A-'
            'E@J8$_e4b3z9u*r8?ZVei5AL%4O*f*S;|ks_7e&ygIH<f5EnIJSO4tmJbvM_T)HZ`^xZ*|G<010kJGKRMhi(QnIk'
            'ihxIj<RiqA=0mi8aAxEB*Tw3x)DN{zo|b}c2{Of2F*?Rq#p04pj<hC)19&qm<fo>(T;vwLN<)adYH{Fm==8c!x?%'
            'HNu!v^}<5VD-'
            '4J5wZR#{5IgJwI#G(<f#hI0fgKZvHoXQ#>I{m0)VG~^yog5x347DdE}_|KL__OqcCQG&QEZXmWs<4&WDezHtQOcA'
            '_Yx)U`8G}BKsrk;muf3h%Z0sSO|@?t{xRAfg4r{3*4D5XgVOorFd=SR!>`J0VW<Ms&C%fLpV^5JY&;7j(IPfm9CC'
            'Uko^5{)Al^c=y!vPQlwi;2yR)>p-'
            'vj4~G`n#KjH#N{F1Uo&PIJ)U(x7xTEPCq5Ys&85dI{uVXZ5Py^NrS|g$_#&0#z&{+cT#Lc8N#*v=;>MPs<QgNi2g'
            'LAG@cKxU@Ipkm(H76^l)YHKjxOye<$Srmk<d&V3a{)Pw1@R@6LUx8;^P8YdbmzzWznoroS?a=gQX``H7e-'
            'M5z~2yn8=i`Yjyd2Uhyd;FT<PBa&4x-'
            'fY_YP#k^W$)R;ahwJBQ0PDZEm4<?b0w`|q|)rb<aWlqJ+JybDjGLz0>HrqK-'
            '9Hw<g(Bo$T(pqqzhq482X1h%~l2Z}P!h(~c=elow%kH*{ZaJ8_KZ%4|=|#$Q5{i*C1RqykmJ76V0KHTzrkFjZ7&)'
            'zfD9LP>dZYXNpPXnE@-'
            'QB;THnOPStC7wcZ<@~Uhr~kE@stOWsxz{f*^1i9FERDrTm)yJno>CF8PUgazpbpZdm!dSasF>1V6Uks}h3$@RnA_'
            'cZqvfDk|kM`Wf7H7}~cgf%(hmJ<Dk*=Zel8IkI%kcZm<CnQ`3dH2uNDCkDtTQ-MhEz{=2b!<k-'
            '9Ja7~yrh$nyV8dZ5qun6=fG^7!n5HH_U)>xpK7>%N&~3qL4`G0YEF4(9=;02&v~z;wJ7CZPZHDpJ7hp;gn`n?GWn'
            'Hk4XvYgGNE}gU?+^b9la=WcmY95k2hr3G(YwI=3ho1#XBLi`q%=!|JWu>WYhF(_vyvJ1-'
            '|Bh}asj@w0s9>uPtM@uYu=|<^))l&WdWDE6lnSOw)0hKD+rxIoP_{x&SQAFsfN`1gj)RsQ_Z}7!$yoPY0YTk0pqt'
            'KN07ln@?{GTnkf+AOCPA!en|Xq*D(e8y4Y0&V8e%I=E~0MBkEw%=(ZuH>LX4Jyk|gTj1idx3B0BS<UfJGIC8)aU6'
            'YDTSwVU)K~!(nd(HZ0RwjIe&0wYL71-h-0t3?JtZyvGGn<*3aG*R-'
            'B=q73f2XNu*7;{YJjcGy_$^&LPQn?Ak;5Da@Wa1Y7*Zj9J0J@ZuL+RV#YV^y@;m}kipv5#)dG#2IgJDI_9W(zJw%'
            '>?@bsM!FET6f)GX%TH}$wd@)m+)z-NJfXWP*7>pHJ7TT-'
            's>7AK?)xPp66i@TTU<n*e#sNaj5ST3zugXUXbF9c&ydzd_Z@F1aa+8@6(49<G~a*V$n1@ASuh<Z8&Q320=jW8Ywu'
            'H((FV3+{~3?pCPEXxRNi3JPzwn-ttPnejAffyB`)Sx=^QL@PAOiaQ-'
            '?H37TVZnV9q9Et=v5$Vu8MYQ>sooSRQh;?e!{|KkN4Jz$j;XdlQ!a(+(7yvAm_{(70_O0@5LY00VqXAyn&HzHk{;'
            '|};f0X81!DhJPORy`|Ix9*YBJ0o^7*2i*9%BSMq&yyhbKzQSurmA>3`#=H0s0u`CtDVJ|(ucpGvpOsvJV(s#sKim'
            'A)(X{<gpO$MXlGhd17EECkGHJp<WMtpS|ILPT0@cnM7o{c?D}wqipW{7O8M9(2G@IX%rEnO15@)dO!EvH|IN%7SL'
            'JahjiN`Tx&VDTFE*E8&?W>-'
            'v(IjC#Au#K#u4_h8q@z&_0AW=I?*1^*o+@A?37U`;xCkkHqR!`3mb1io;j4~Hk|NT2H~c$&pfHC?i%#?aBnLrw4v'
            'h-HW3rt($<Y7%^wzh)}(h9<G?`M7L|Q7{G=J)*?mflKZd=n(CzHKhy#=--'
            'IQ$S5|{3R0k!un6ws<O!j(p^(J?5WBz!&GvKOAR)*zXmz$jSvD6)E$wTJty7(GfB|c?Vkv#^J3OG{0i&^w2I;A=8'
            't&vQ1QsuUF%BcQ5%+LO!Fe8Q(^oOKXjy*iva5#U|576kVi(?6s_yiZao|5a!mEedxoaF3f?KYt%gb`rvPcG`F2Qz'
            'gP2kcDX;k&;hL3u2M%`gaHk+5cJu+KMMLGmshK*E71IFw(hjcoc8JK~=6L4`O<f3`8*c3D3cjH+#e(%L@h6FPjdl'
            'x&tRMFI<@gqtNd<<zA)#Tt^gcMYz2X*bbbLjc7xaQXqQ=Yqqe*vQGv{Rm@&%anYKA}Aer3}#9LMLIj9X1CxA+=c;'
            '%yxa!lU++fK%Vk?23OObV*)%fWD#I~dm9jfGVoW(nD<4kHiUFIC&vT6c%gi_l<_mC<eUVm?<wJi5a6an9mot=a!L'
            'XRBNPKM%$7}ltV^+cV8{Zfb-A*EI#kagnVuwMP?3}GY%*qqNCm7~e5l`Jq_UxFtjck{n%J?xm~${b0V5bu=K~$-'
            'SSBX{8;wB1l**^r=q+^QsI9V;Zr0SB)tHr2^%0D}xtP_e#9WcgfBh6_`i545inyt}2!7_oZ4pWz`;nI~1I}T9Fx}'
            'e}rDX5=)OeOR=rp~h<wH^o=yc~qFKa0rt@&}8+?zs5RG+E`ni>*F`*;`vKl-!wWVBt`c$eiXF-'
            'vG;vsGD4ZY0Z&AZF{#qE~UJnMFdN-RW{>ar4@cFBBnRgqr)7=*Q?{@C1N$Tpb4xuD;%<Rcg{WklUT`zM?g0KMMeR'
            'aF9I4{!xL9ZBhG<g%~-E7X1L&K%G4UHQ&ia%M&R>tZlo$;B+~QxR%KhzV%c1XWH2bU;?v5-'
            '4MyqHG`ZMyBKMOjm$L4-'
            'lsrE5@fWqMQe70q;D>DkSSk^nvFo(ANKcqepsx1`}hV(Kb4mKQ1*vSrSpu8b&3)BKL`GSYSr!Gme*ZvLvZdsB2n>'
            '^8dg|Q#bwsZd{%xaXZKP6tQ-NU0QCYO@e|?>s-'
            'PMi9b0N9HYO;&Y`(76Gx;*c*V(q{bg>1fF$b96R*Z87!;lrH1CP;Wo^TtSbZ*@_=5h=hOQ4(NRsM1w?}swAr6`<X'
            '-X(8bm?*jhf<JrE0{kko$@`0hpH+hDf*JDXMYY(Y)e#@KC|1Md$HlCAU(&-O!I8!8iDu4-'
            'U!ZLH^s1UoRwd+8qKs+-'
            '@^uRQ%<5|r<%C2hZ6nAEAylzi3_bZH7h_A|4JAtJoru}$o(2JvZ~)Zz#j2ZGK#kjK7f@@ETvmQ?=p>ZlbIXJNmo!'
            '`ZB~&Xbg8#{G%!pvmNNBGv1sRp^iUxulAWP|BF0Ke0*Qhy+d3z&@mx)l58vMs+I$X^Jo1xKJO|uodL9}_v(J{-'
            'UIYeJVk0e2KlcP&nP!nXdTX4@6AfNAS-!SW$eK`5MCdJk{LSDnXn~AX1ROpQxwHn5*409RAtP;-6od@lS)-'
            'pmGhtW0sR;!8|?-'
            'kGtQ$nMV72oBcM5<HreJFEN?&^Z*7_yBuwHYnr7n@4wY)#4&l6G2Q7tt<`kwLVb$vZ++W^QmC3Z@R^>+9CMq`^jF'
            'h?7wOU+wP;UBbA!2N7I5ci-C*qe3tZ!3s)p&FcF7W|`EB*$s&11=gGqLe@n!gP0MS`4*0W3kqf5i;dt{klX-'
            '*h~QS1%W?yZ_~Pnk!;r!k;j<m}*>Lu0#YJq!YRj|Pj(1aV{0^Q5nFc|tY0|OM%1EL#Zg!Q<7KWUK2HsiUZymj>G3'
            '67CAfMY1(z>3IrWrq>Ek=#|*e}}mndS1w`yI^&kG|fI0C{j=GK|pF<3@$>tQFix`@Jv&Zdy$;adzCo)AZTCCx6u@'
            'j!s;@m6>O~2+LK8y2-S=CH<_Xzju3I?T^mMr@yFer}MRFkbJ0`O6*L!yPqX!mo`&B50huQwiJ#Gv9u-'
            'Ts<jo*2XY<Wn;6=3cn;csU)~(diuuK);O`^;@4NkT2qqNcG$ogLl3X-*EK`$`5=%NJVh^pma=6fef2w5Zi*ihlJ-'
            'Bk%tuYPv)W=e^cRfq(GcgjH>^KefPqrYkw*x(HbpoYFm>$L`PDb)UjOb*@C>DU=1=@6G(-=60WJSHx;zLR4-'
            'wrufxxA?%5_E$PUyB4%M&g?te#e1TIVac+tE-Z`)1067$e?pIhrA7W-'
            'ZzuaP6wgvpRVf!b9Nhr<n&K~If#5|N~n|CjFRcBF5oKtm*IZgP0~`-=S%<;V&|K6ucJ!-w4Pto-'
            '`5{SpXUNYgh#9ev?!q{r}*c|rn&llvtFB4Myx|+Cp<O&vYQ#}hnNce*S1m!*xNx7q=K-'
            '&1P8k=DznR@$HRRe>`IwO5p8yZi8w(y<l5$U1Vk!LuA?Yj>)4z1(8&3EDBBGW5A$aN*pE&53PBN$U0$gM##GQWnw'
            'p>98oTXMY)yWFd!yPK+hw)I=NF~eQq@xKvE2^dhu8T<{ZX}(G!np|LSAUwR`AvsD<q4<-'
            'GBUbunF&`7<RD`j2cU>4fAC^n>o!f5j4n&a6b0k{WP%#8EB0Jkra&=ZA~q6GqFLp9u1T@*vxk5p`I9|Bn<F~X|$s'
            'm*BghfGD*Y7#&i2d`{~j-2c{|6YX@u-'
            'U{g8BuF%!2jP8Mf#+ybkZENc$A0RPY1g+d&vh!T0fDSYU;+o|2(mC*ReL-'
            '3I<l$~#oWlq}{K{2&F$rJY7f7zUfS}{x5&Ld&5*2Uj@Kp@$Y}SgIctN{j>0JSdrg1n{Xp1#FvTmv$tpOe3r3;!c)'
            'GDAsnnU)xap0`imVs+`crw*}ob3QT4d=Buy%47w;d!|6nMn!tGDZkiKQ|N;^H*&{=_tPJPap@EB-'
            '(cU{^;hYB!wxXB&kN23QKn6Q<csoc$BruR8NYT6!bvUBm<PebXhcZt9hV+sCe|j?beIq?ul1^Lft~(p(thnAm&{a'
            '1;9a3@j1}%f&MC~5?&1f0QTJ>^kE-{x+VhM)o;O`=IDa^w+(Mx5<yUW{RBXmw^Ohy-'
            '58Pt<n6+c;@3|cl2RoE)!Sg)TPXkouOyIyxu?3KL|aM32jNmMN)=(HU(&ihD^5~k)C85aJL;3<M{(_D{}xU{{a?a'
            'CBlSYElYv`N)?h6>Xw+Gz=dEhiVUK%+542sbPTYW+_?GB_Yi!>ZIslars1aKujg9cl$lhY9ub1jxH#EqBl=%xu4_'
            'u<zkRW|N8jWah@F-C?VZG3bR8YvWU!4SV^iR`UP$w8rHq7bV=6C&DX^G2BZCe(+vY5rX;LF8dop-GoT<spwC2GAA'
            '5@=xC!b%|W-'
            'WJ7u=_t;7ts+^f50|8~i_qB}d*K|7rgVSr<trd*{4mRmR+c`ojj%dJIw*j^WG<R|CZq;1pulAGVA}#=Vw8#UjXU)'
            '%TV^iN?`#zckayCjpda8oCotP-&r;Lcm*LDWOn0H2(q_j9-'
            '9_}i&qNT;v3#Wv6o{MZOa`GTcRjn#Dg&PluI7twm?g0jLu<8hs0WLxaSI1!9&F63;Kv|#V<7;?^cEJT4!nt(Xyr!'
            '6OR|_zo@cZL=bjbCkm{W`Az%|u+p2wc#nCQtM2b2iK}2MzYdpiD?T`){_PRzQ^}I+rlV=!CqQ!ebq&%VcOM_6BW9'
            'o$Y2f4dlJeViVF5!rSH^^|p@jTmKdeM;fE7%|`|E35fueC7U$WfxEi~9y8saaReGx`Kmx2;rNrU-ipsmV}bO-IRB'
            '`vc`BA0>Z)zv}nmUyt|iuyB_L+}N=}@@SvRGpJ<;!!aFVgeinlk()%Og3aOcAd#y#$pyA&B2i&6Xop_ydn69<Aek'
            '2*`&%Y9NDR*;B+wk;|CQyQV&<joR%DAOcVcKl!-NNRqW7(_3~*A@pXv567iu^}IQ{l$mPq=T4l{iKQ+-'
            '0O0mI37B3zfv8C%#VwMxUrN&2zlRq<)t!O}0!x}T}=r?gAB5%u|vcL1{g?y>=0JQH|%N;Z$7OuT$*WNK;PriqCNB'
            'v-'
            '|ymQmY0*|H%84A0_W*R_y>#zOXUlE_nMUl8}S+p77A<0+JGYny}(%Pd3f7!zhV+|{C7z1@{Lq!?v%UC1KhA@4<)h'
            '}>q95gTB=A+7Q}gqxsmGF-NOtHW&9@UmFUG=T>%;~|dlvYxaAs|Hsv)IIs1K>a&Js_HrLEq=P0POFdobh)@pw|0@'
            '5W51F1DbqjBrAEV09375<8X99iUjD&US{$veHNG4dg#^e+<GEL6ye4UnG*@c}JxObC7O++T7pt;(-'
            '`ffr>@`88MzGmMzVEd!$`$-~AR^_PZ-Q@bS`-D_tDm($4%n_Tw5bo<mm#aT<Ah`lc3M}QDp(if;zOMkhEB@Eu5x-'
            '8xxG_IYg0i2$3+6Yr=9w@1dCh2eChUf+13_ewWu46R*JK>_5h9txkmsgX*-`#$OATc1{C0NN5864cU~cdkenQI-'
            '6T?#jv;V!LF`I2uY)z#0P<5{`!xFYK^;|YnYBK9z_=MwU`8xj1Px6rUu3;5x1+jJI<*eP#CQVteQhsZUmd(PghC#'
            '(^7N{1Ihgw_y~NF29eLai@_Q#?yM@zB+m@jI&9Ys@Z$FArsfs0T|MBN<VYZ1bw5x+@hZWz$$}<gYg^Iq2yNG?QZ!'
            't;w>WzYY?TRx(>x}x81-r`k3$m3x<-l`GM`-'
            'boX~`p@7>{<*U=%GPg#m)4|C%NcK^PYmR6AK;i=oDuohn_1QQyVl5;!FH6T@y6LQUNwfVxtw?hjTUylHTRth-'
            'EWAqDQMr}R$v7^{vGw5<T*ca<d^-ctm;mt-dRR52;mP{KeZ@%zWfVXEMW7O7Mi5m)$W=M;ZGfk-_7v*rgV-'
            '@a5+Ox!NmrI>c{N)Twd0=n(e1*-0yRm(0-'
            ';j(Jb#L;y=>+O?h5hP;?37o?VW$`reQaxbG_<Pfi;5Fv^#P`NT)?2qw_2{GInqoEY^;OD_S&Tr7YxxnLy+z3FuCa'
            'EEij7KP?TjbptGc((>Yj>dObHDaZ`|UW`a~a9XEqlxGunPCGkT_Xe{PiR@~V2fH>>Lsw9`th!^tt%VLDT5Cn~7!z'
            '_QbT1txM{-C-6|HThAm%UK9Vl(!y-7Ug1pV7XS}JLZbjkU-'
            '3d8cz1S(Bf}{k6lJvP5EYkyS21`%9y_2Oudi`p$T*kQ@givK>2RCV4uvAuO1%z!n>02?Ghn~?UruA+VOuSQ-il=`'
            'lXYYPfa7Y6aA=D^;>xtb&><PnmB_(<b_+IpX1SsI31%3jl7B~<;P-'
            '7^_TFm;9i54bgTz1hN4W$^WsL<g~exlG%fv9Py9_G$DLoAt%_?}%gC4-'
            'ggr=5X6<*5XRdV4d%eg38MwmHeJMn5wWaG+&H0@iOhbwT_=8YL%vFS3QWlJ%V3;y!t{)89w+EEVWv@f>&~D+x95B'
            'wLGszxVA=t|}+JAj2bEsPx)pdEXtgS$|7tE|S%gAmC=?_#xqQ|g%(#w_;3(@t%bB+8siaI1xNH>*4r8%;gmi+7lH'
            '_*o+(YqlBqtO&aOeasZ0cwcJFdKF{rH-%&EfpoH(V-eHNv_5QS(RVfM{)ahAITznJW@izzyzoZmjH*Cv-$$EN~-'
            'UTP|)wbOfxUgnt^mjpq#Mm=nyOuE7Pi3cb1bH1){NuSK_-'
            '<u`Y{g!m(If_PvrUTeH;e#8=^W&R(k+>&a%m<d@fQ+-6wOj`-'
            '7_VrD0=en_y|_IwF3bh8`5WY^`Yq6_*{SgZeb*NVs49}1}oUp)7N+%)i(SFlmhE6a=&-'
            'jlMJU==q1c^2lx@gECQl6(-CY+AI^Z?#{05*GtwGu#ZbA+NQ{Z^Ph#NyGin=S<-'
            '8GZ@1APys4$#3m%)9whraI?XNq_B+kqM=?=c9kcSI;H*uX(TiUGgNyYD+Xm81_y+B_<#dBpy4P4K3Tzh%4u!`b44'
            '+`%=1JV`s_<yk$#N7DR2H#(s|ANbbo#KkSM~ZiB*Nf3irGPzEJPup|GNW4sv)`F7OS~xQf}~tyu=bpU3}BFC~s9@'
            'iUz{7WEdaVS$DkQF4ds4W+1TD%!D-'
            'E7v~$EiW5WS<7d^O`mLC0J}u}806)48XO_56{&4m5M)1;ONcmm1CJ7gucn(r9{J#%^5l?TBZwo%Hnen}nDu7GYYU'
            'v*I@WJkQb`8)n9m#K5Q0*U4D=nTrC11&!K*~zLC11U}&R{AL{n4hl1N%?2q=hDENXp?+x1BiGG&4HA)k9|QG7Hz4'
            'FlBuy^$>M#mx@CCVi09%_OlMX0;h*_WHpAw?g(~gEXZ24dWHQ(@;|t259RiJC~Hs{>0hay4+~eAMsHS+F{3}{;u1'
            '%Zfx!_rlg?bhzYU>_t^slXV*6Z{pD_q)r<#8DCV1Hsji=V8Ex{DOj3z?tlJNzpkzzZ|`dQ$isr5R$=h|~@{YT1PQ'
            'gLb*yUfitC9mKUhxR;JLa{LOC*dO!mG>QueJnVO36RXTDnXR8*xb;2-V0a89`CS$K*-jl|GIlZg-oSs<KR{!?=Dh'
            'U-'
            'k2=kjePa%%aQ7DDkng{5M+MS2nkaa4D@cJ?;&4fQY1@RL`~X<)f;EbAA|{$q`n}*V%VU*kw7~WJHHb5_~rsCeEs|'
            '3-oH_muVKE2g}%}}#b+h<%raT&G!^aa+F_819>59$`8^WG@9%QEf-jxg<z$*VSeZjzQLIP$8{q|%*8=L)yc8onJi'
            '*GRRPML=`y<6zZ5S<!@}syh<iX|ZNIhKai<X9Dr1VLJkEd5PWbG`pzK)WLehw)snvisW1tkTe1lOc|Ckde}8Zl4='
            '0WNJGm+T9;J7Rh2D{A~S*@lszl^Uv~KxjtAAMzp^3Z7O8d_l*BVvmns;E%ifmOz{N)p#(-'
            'a~L!RsM@yk`a_uue!af&@a_CPGPU<mB})K><#Tm{NAm?Nq-'
            '(_*)74s9N3p05njWosP0qmX<2>hQP*24l{aA@ZPc(4*ujbgj)vDq_w8~}n^0!APuiu{KFOFXQaQ3JC<nZk5=<O>y'
            'RB(M(vU1ic{r6v*FZ=Hv?4AE>|6fPHOdi1h9sV-'
            ';GW*y6fd4+o#D{m~(K$AOzyCGk!p14~q_g?UW`F<UYw>^oa54TRJ^wNjzx_XHFLP&d_B#LZCA_@iZ5kzyhWq6=By'
            'FT~=kKxn@Re*JKm36|Z1{uxy&A9TMc`9oeOpK{dlJr4eNl6%X7B*)>)}`WLt}rb7Wns9`}+!VwHRLoKbDRA`S<DX'
            'jW1rUb!NcmtI2T@T#cT~x1NF<<tKV>ENCB1LYno|3!wz96QI%(IuvjT2`+poP7FOv7Fvk`m3;T&#yWZS+{ocqHG('
            'tAr|H;l$lr_-mbCZ4l{cyVSr7w%rc#r|dW^DdkUEFc&1{BE`f?0;0I6fpMYdT~^kz-'
            '87+$XG&9eVE7#2aIygxcpBtG&3P?mzvU81hJW?WFzCfVc6IXud;<VyzNl@uUH!xVBOmVE*ebXrk)Q~W(t0G35uA`'
            'vwU+9i62Zk1zIh083@L8ziUN`bnKD+8*c@XKOVAo(P>G^+Z5w*tJuqq(^P->pST&~B`Xu3vzFkJKwrD~NP6H|x-'
            'mXoVB*SzF+u<4a;BW+K@wc>kQsW|E<yh7swMcb2QQfp^!JOAQCKckTyl${mXfWR~NpYp__DK*zJA=Z8POIFqz~a`'
            '^V}<&ijL`Lm;^$1e|G<R>o<pB|kCY%R}mBFH(E-<25$CO2P!bq}O{%yK?nCx@p`kB`MR(FCoFQ=`y)9A!;-'
            'fVZ|jcJfY*w-*can(u?P*KP=39+7C%d6QGY{q(9CUc&I^n+B<~fLNJz33d07821I=6iB(ef{dB&RxA4K$k&-'
            'b2**Iy@Gqv-fwMxz9#wP8;;n(m#E%@iBhDZHHX7dAAn&HEN<qZukb-KhN^T4S{xe*$u)PmlUkcuy*o}Fj1$juJS{'
            '#<9%t`3a^~r($i%X}v@}wGLW<h#auRSyXf;CMQZ`o|dNTGlE%g>`n$$UOYUW^`#|NiAKM&)4WI2k!`K^(d3X{CC#'
            'ru@i5!JVpgALX2PgD2<WKdg07QD<7R89U3220&~r^9xI-3n@KF5#I-'
            'hZyX;ZxY7}QAGzOCKj9ri+cGLeeaia+Ao3a&fI;#ovzm)`sIu~6&BEshgbuy?D`!?AYb^3D+YXNV@D7@sOBg2E(C'
            '^YeIIhdpI6yM<Vz~sGSrykh1xScw$Y1Q+b9gk~eESKf=zt)6DZZV6MZYWt?j=na-BwpcgVrPbA%!sNCT$CKkaG=&'
            '`=IhWG7`}AVh<PxIxUSD8N;_jZyv!vEaB=+G$kRc%U#DJX*R;GH7<(^pJYOWf<|Jy>=N5a+MD)c4lAc)RjuqK=*F'
            '%=qe0TgBp(BuT1M!AfLizwo#l_+MZ)MXZl7}^WalhF<KK_Yv+bwUurJaiWb~{ZrzB6I(-uF6(v?zJwcf?>-'
            'bUAh^l)yf0~WWZmV9iRYQC9~72Q26O<!{D_H&C`d@)Iun~PaBPEHlXm!kVKVES4VqsZ%8&=4$1DlT|WDfZ6{qn$A'
            '5p^*+iPX%sI<S<Bl4FxsZpA2GDPnG1Z$kh%^;Gx|ytGH0pYzs%nsQK09W{z%7m~TH56r19#4i}T>Lib&li^-'
            '2d5KRYJ7k9g9=Gn@7X_oyj)f}?VQVqs*#0RRa(ctWlYOA}Y<Fsv6*54Vup{K~mQzP_I*H&;?X!}*5G-'
            'c+p28HkfnsP0D(FSDeOmS0r7aBpJdOVB+W%a<zT&T__TT_2&(16O43=L>0%si3}K6mshcR0$y??lo_D+E|T!DYjG'
            '#6v=uwnLC4r$$JKNwk_F{xRl<p!lF}!%n7%UCa=c38H=Mm^C0~lSm#K`mrJr8-{19a2jx#T$}?F4aW9L-'
            '3Ep(8$KSs*=oS|MQ+Rd+K5|ir*~zIf_u27anHWY@S~?1nif=}t)|O^t*62OueCE5Ol&i?F?U%D4Rfb~ZEVP)T{zo'
            '|=K3Q?tV+8`XJNo*f!xSMrFw6Zq0>0qZWZVL<5}Gp(fkgaflDO8UuOBbo*kg2_|d)*esIwkKYTq<1y}G`;874<Jf'
            '|TmabJyPB|R+_jiiF0MUw$dQv7rZS((IK-'
            'r)f{fv@LAY&iVshK5sDt}7><=924zNSp8x<pnEU+OpxWLM!L!;+mfsA=D<nxRE(2w4$N}NAqo{n=I46Sb0E8MY+>'
            '_Ttzc;mE?Ci;vCnFPzZOPdJdn7mYdPmLPSCybE;VfY<_0=tQgqFM$diF(8eY`5$1z7^?9Gw5bw53>U_}hSi?$IY9'
            'gl>c~ZesmT}$GMUl3AxU0_|G?r#g2=Xx;uRw0JW<y_~XaO@$m(nZ>nqd)RVEX<XmEpM<LRBl8B(HyZ3H#b?=2Wdn'
            '29dE+VK|~8pr~AF;#aZhw#?{F6y9B_ZzufNQOS;$ZA6wdW5~h#e8B%VJyUDY;K6PHPD*<~Hai+KGap2#z;gdBgcX'
            '0HX|JC?KY9rgq66?D6s4YsU27I8{4psZJqJEGTT&UtkMmh-'
            '<YDQjFKbW>HuEsF>w5J*rEtr?4r|C?XGUdlyhpIY2&rm<j^2yyR-%NF{CHlh-t$3-'
            'JyW12=sd7{i>VpiwF8{yquy_T`Nrv)c?ul?(lN_hIF5HC<056U>juM<d?tbTG(&>ic@0<iG9dkOSbvxc+Jrlo-'
            '@DMXBK*PjKSy$R1dBny|0tZZ+t;a37o-'
            'oUS~L)5oZPA%zB3OhSq@}gj~Hvi;@uK=!3i7mqg!HSJvOm=3$v$g|CPR~{ooeFH^xa}dB6nB?t(4A6A$DM6z|1^M'
            'K3>6TX>M=;OyWW44G*U=;g>5<5Qa~!HgEBjx#@AKx~{!?k$+25KcUH)PVXXXn0y(LRN1ja&TY^Mnh6u%T4mv`ohx'
            'bj5x2r`L@o1it-_b>qf=W*Wn?zdX0ao&>$lSMKhpk;^*)tdBoC-'
            '<M*U9CD7asWu%ZcR2@%D>*{&0V?rFJJAX5rkac?w2mZlgLIE)Wx8|VlB*~grP2&ls2YB83_j*XWioj!HHG#TAZx$'
            'pPOr!xt?1|UNAd`c>$s)>yxX@Q%r6QVC0d~A(gFj>gw;+gWgM_Eh{1!humkivV7U2wRI>MYN7GbqLSaf9v2sidAN'
            'fS`t8$Rppm|4j{VYHI$G}S{Ux7K)$Z(eAFlW10@Y{$Dzi}`T3wHb^(#0{mg5_mAV4I|dDw|AcxTgoA6p>0(b+mRN'
            '!j|PbmJ1h`WG#H~Em!qSk7OXQup_ieBI;SG=&fHx0fqg{U8Z)!<#pr-kBlk&iBu_02<or`uJka<IHv;?~XiR&Je9'
            'RyCpJL(%vznp-'
            '5gAS6?03Lq@d2L0gs9kJH||85yOQ`C)1zikIgHH0s@4*lKp?tg*WT@jH$X3%SSn`Y(1S@^hMzbWVeoTe17FU)>G}'
            'oa5RoV01ogmg?<OfXMto=YK3A$iFOX2j1Dqw_C67jd!sy#MiqBPeuUzIrq>)TE^s=KgJYZ=ADq;NzuM-'
            '~PuR&^~d;HeH*MsEI-LNg!ga71N5v*JtO`Ylg3%2er#aBqF+?e8Gy#i@i2H}#_12IO*SjFTGQP2$S$EKvD2C~f_o'
            'D#ueuZj<qAV>`B)h9!mzkIID@X7{a)vM-'
            '847*uWLNHd|ndBAJ*G?`sWzz_BH5Ey`K%^KuQ57?9f=nAcIGUy5Z>D^sHp#l0&GPPN-7rh)nFyXyDRhq#Eu-PT1_'
            'pCb(vq6lo#jH*E%lTF=39BDXgTlP3BA*^IX^cANB8)c(EM{Bcy?|aQKN6<e17gj2ihCZ1jQrLxrrUNTXSh}n84)Z'
            'k~5J#R7l?l(u6loVQ|_fsp*#re`7fPxPlk|+Y+<*2R1-|?$PzmHrl|fF6Q+{?1QfjaTfZ<hOzH0q-'
            'Q`N8Q$x*Nj^w90o9}DQq(X?S9*emc`2@|L?#xSQtq8MWBp!?jdBSMmFQvmJIvoec9FmJy!g>J_0UxfoxfdQhoK?T'
            '!r9OiScfTcg|)}vSHDw0MYP6_w=<^@)FKH^=rqT;odMBQISG*QCG(6k;BfP8GrO8*WXO_p1JI9utLu5bh6jFYk|V'
            ')K%E_zPZe#h~UkDuy19(X_=H=33WNH4E#*#gFw=+R`cn=>1UjUND?PvOcVl?T}t4YhF&aVm?f-'
            'hRTrO3K4YiS>M4RPexa&(~I@~L&FH>bP4$2NnLOoM&Og!sIi!<y6Jra@j8u<LUaDR+5UQx`Kkh@xsIkja{EG@8kc'
            'WU|3!qaB``N@~>^zyME^x};z=DoYGzVl|OF^1!XH&=fQ);Z>Sf5O!Ux#F9+sPR~v6=2KS(XAj{p<nb{^+-'
            '3bc(tFS=r1!O6RhRILTP|F^U}jzrSzAwf7%(s3_zF@8+lA(X#@e9`3+_~ngr4cSaNt@w`MyXFpPfEDdI>tj<Ne3q'
            'BtK%%SMqrHNYF)dRiRu4WC2txHXrg03Gx7`O7b`Zn2b{cNp5{5R1(SWnqhKiL>Q6{8F<+S*duBc>l)221~lu5FXg'
            'qPT>}3ithpdwiN}G0p|GfqfF$QOH0~Yqm^kKZ@A*ADa7@&Vg2rKg8!R%|>3zI=5gDh(%o734OpbU~A5n*0vYgNbY'
            'h0|AlydTBGoKey+EJfJ0fA^BP`!qgqWFNxuJMJ8^Xx@kJPE053g*zflE~-'
            '6=Eg<MU%W0s@ke!n1x33AM4g^1hTA<u;!hU#T}@NtI#lZ#CAaF|cMoqpbXnE7r&t`Gr(y~h0*XS2)5DTMq+<vcN`'
            '2s8P7l3WvoBcm)h~CcC58p5gv)_{J}Oa9+`)mqH>DTbJc?QwxazL2%Gq2ATQIu@-'
            'X3F~b}d&yQX@38wbFRiGRe$H;76Y^dS2Saw4V<ge11J^5M02POrh#hW6f;4o-'
            '~?`9`B!9b~vI#W%zpR<k~{uQmve(!{IRL-&%e4pt@o*uUBQ3dZn**E(`>e>9^SJ=S)um(HqqL(-'
            'YfESwu+M)~p}cDDH6D^~D>Uw}04ooje5Anx_l$Z-'
            '@ixdCGTMNQ?(XRuf`Coz`(`&iwdUBdvOd(?l7^+y!XrXrBmDZR_++H*|Q`=`+()O`iMz@P{`5y&HXfo>@#d{bj)&'
            '5VVR5bRPvSArZjUdd?ANe$EZ{<74h9dBeWNz9-'
            '_F{xx50<`?A(xtLTi^$427(QjeyH?YGK^G|$eYD@xi_TqZr^&2rs^}6;ao#Qv~I`wUd0Tdv3U9ZR{r%Yp4WdXmjz'
            '=jGiyyt`^8&3dhnm2yMKYE_CBu)O?;-'
            'XnT5&O*laP#s^({C@nyM>(^md&_W$^cwD057}y_Tj~M2j<;o^=W<c%fSdS{AZcrMr@DZBjuzIiazFiH2gp6u_vMf'
            'v!H;yYNvUGyowtkW!5u#uK2~Hi?7Sa`>E4FB9)s9iK3k0$hf1_T1>zl3$=)r!7l#$qw%A0=fRF&{dD-'
            '^_?aB874(1q<JVvBcVCChXE&xi)YbaN^bn?e6_Yr?F!<`Xuq<mhIgV-'
            'B6RVUaPpOfRdHg<iGConhu@$uaZL_|amEVc)7xm;OxxE!Mu~-'
            'WsWnKxbL0l7yX0L&?cu(jD$dEZo{$=>}a{VMhjEs^mgnsqt@mEihJ8%wMJyKAp@gr<2gc6}VjFNrv|NUY4G1=$lO'
            'K2^Be58K(_90K~+p9<RfiZaj92D_;@7v{f;#^79XauJxu{s4({-7g+jwv5j0RjV?=p--{-'
            '$0Dk`FffJWZoc17N#tC4SzI1hWb9O=R(b-<cenZvHosA`1auvP>~?!4pKtu-nw3n0OL<mz>%Mfph^0hc_zWDuP!v'
            '+>s#|M+{tY<2NCOVc^vi0?gAUb)SJPMi}3_WDk})xb=RwEU20Yb*@}n)+Owgz+<>Nl>)(av|0%9E`?(Y)ODlx3zX'
            'pSXP}|ql9xN5_G24EtGD)7?oK}<an`A|1q(JQcr72l@2@ul5bpmEGO8FpDtSN&V`&_`7_Uonsr!77?q&zV)kvF74'
            ';CT$+te*;zKB?xIb?MDps4F^1-kb^^0{>lydi=1dWCwl6zIh6?sqOM_Fwv*+H*E8Z;-'
            ')s;8Tb*#vOYn+1{2cBWcoAEqxlU=$vmsaXdO~UeoTyoEg`q5>V|yCuQo$1v6vNXB_Ow$G<%qDY;W9r*h3SMOv<HO'
            'W61@`p=A=$oluZ&E&9LnI=(G2RXxOsJ^Fgz{Z*o(|Hl8<Q2yh1GJH|4p@OVsue71OUV*ET0@4h$4~_4`7sX<NyrA'
            '8{o4zrHd?>fWS%+kvu63QvBq*UBPD({)OWH@=3HqmPW98q67o}ijeOf{LWTy6PI9s7JA)%Gn`3uu5_<Vh#HU&h~K'
            'Z(Ela-Ku|ZFoAb>-E)1^>JP-&sO4I1}V@jnN6YGm!<YBD(T&J=i}-'
            '2le_D_Xo56$bWvWz28J?KZ!<@0Dc0UY2=Y~uHVG`-'
            'qDh=^JkjC0nxJu#o}2Mx@nhc!!zCrDtS+zCZhQLbcA&e>ZM)KE2j4~R4<A3aEf`C(@NDh3|FshqRl}VUo}u6S(Kl'
            'Yuq&QOw9|m&vlE=e+(TCP!<B)Zq1DlUIVg1wyX!K7?$FvH>Y|%&k;w%Pt8bs=%C_v!`HnoJ?U<3^kdiZzml8+4)z'
            'VBOSj=XrVQ}G*(X4s3Lk%p~pwVMn1Z?h7Up>8hSNMOLdvnYXotmd1!2f;ikNZ?-'
            'w=9y!1A$YeOs#FL$^CIvcVqpSo5M07`6zQ3Uaqy)zMTZG6zb!tvk5}YRYhbQ3V3KrT27GYBt#OFHIo`k;J-'
            'Ee_RdM~4cD4yU%5mflC2OEi6h2cbJz(b_EYcc8%H9Xi8zAboSAr5zf`bXk29R!FI+(;#=nwb;9vSWfXPX~LmKx}&'
            'D8VXrp;&5^g@%HLHMl)vT6=O@dp3t|TQl{(fR{U<((}Gaa#FAd&K_863gIbOA&}%-epRNp=8#}TY8s-'
            'OKh!pwsz;hd<ZxT6c&YrR!>W0;nazSlkuW<M72P;sNuQFnGTX}9y70*hSJ*J{&#*v+7#`yDu(u$1z61#oa*i9{Iu'
            't%6SG3;K?ZbbJl-PWb^sRO*vp~H%W06vl5nS_e>>yiUZaNMpZv<yNby2hp7?|Mph7$6i1C}Mv06t0NMtJ8F(j`#Q'
            '5Ufvx7(hy4Uzr87_CaBDEqt{%KZ};IG+{(`Z_!fy5@>eDk#x^z#U=gqw1knPo&E#5!IZEE$`bWz^7E=#hU-OcmB4'
            'H>VzdtUt6Ho7#I7Ldl>1INQ*70+p*bCFm+!+{`1SOgKYa5qX%@a`;``BdWSKX|MNM@xbh!<7xMH_J32Y83h%I!Hh'
            '2F@XP}IJ;sS(TOULdG=ng&%gw1R3OJN%^9i$IYZ1x~WeGC7&`Qmk4{<`1panu5CenXQ*!7mZSE#qNONz|+%ZS{gE'
            'T%DgevghME0{s1=92h!S$6-B%v(zR!JH_XP4TSK;H_XIf-'
            'P49pL2T2GfPgJ3Xn6p7=X==(`W#8(He|<3QqWGrPs;+~}6Roi05UNyzP{uRGkDx`W28Rq8Q*Ije0Hd<PL3#{yK(U'
            'gu8+hq~QF`!r;>I&1!pm8Xi%?HC(JVGJBM@mK!(uW~YwM?bd$LD5khKL4q>=XU)!~ajpB|s)uMS@x#ewLE$-O-'
            'YQ`%eCdmPPVP(2lAIY?2`&DX1qS<2fT`QKi@ehKNDj{fJ_(W|pl-SDcMEf3OZMJ6sggc07n;Omk?TUcczS!z|Lky'
            '{H70pBkuVuM#kn~xu1g|z$1B*x8+1G@s2lOA6#>XkAjKb#dCNKbC0k&|9-c6u@#+oP=-'
            'D?$X|`LB?2KsmzuY?B^|i;T~*WA(;rEfB;9)^akxVUi9aE(&91yS7;~3xnRcH3hS-N_6|8T^ZL!)U=#!$n?{<($P'
            'qm^fNLjJ3in4Jt$Dq*u@N9ci!;RSe0YsiP+F$HNK)qKtM7^=~-'
            'lsJ0iIH&HAc_;%eo1v*xI*=B63y54t#%>_Jw4adzKRB`Gy$aX=;|&e`qsW(~QF*I;mD%z%Fp|IyOafNku-'
            'Q2q=oq@Q{H56yaFw`!jQ<CKdJ)vCrTFk$6#VvK40jQcK|+$r`>l#p}M2&nIdrDR$|@Hx=>Q}QLqiX2#w9x$<)6^)'
            'r&5=xu31n{#9NVM`jKw$Tt!Lu{2iqq7}@$-'
            'khXT(BQ<s3^^RGRy0=TDnUW}6F!1hh~is%qT?d^Lv`V##6>$Ln(blU10@qy*zDm54JwKmj%H<Db5-'
            'KYA{n7vPaM{(ec<sAy`scvkhLAeF`gd9rD)zNd=phVuu`7_Bb+71m|^@{=<!<)JXcKkzZsb-'
            '6TCL*jS&9FXht3bJV^FP`)i9!pa0GoCUtPC#(m95SKhITj%g)aj*)D@&|qr`q}zuCau<I#5<bx7`HJ{SDc|qfL+i'
            'sn#GT30E2O(?EL+Gi!~?wB?on2$JelA~4DkWyy7h_;c<(XqFjVP@%~K&&uql$7)=m#{8@+rT6)f0&Sr7^{OpQ{?G'
            'sV|Fk1-XgcyNuwom)!13tO{{A5OMtbwYBV&nqArgZAV1F5k72&_b-'
            '4EC6RdoTyt+6Liw)!;u`7nQ0!aK#+i>Ht&PdcS6NHe5*Fr4T!KxF8=78khRjO9C3I<tY2@TVyAU|E4{kl>NhC=^g'
            'Xel)@)RJu^X35nzaYEEj&T0?v@jBlb&Wvsq{Qho%sB(@N$$XyC)Y$bhv0f1LRtDAvl2O*2~^^@eekm|4uCA~L>*9'
            'Ml5CuIT->Mtk55Lld)8LmmK8!sf)NC3vqKtkYNnR&smJTc2if(peAwt-'
            'o^=HPz=z4Go7LS1n2ib3E*ZB+fQk?0aksMrkKl7N_mfCS7YjK1yg)T9OSI#Fid?CX%B@>GrM*=7zB-eV!Nk`8O}+'
            'RRU;MWNQJqYLT*m#DItjX$9CCC1~N(Y$Ydzcs%^Fz=tf@rrzqd=*)176FDXKOyx04a!{2{)AR}Jdpvf#XGVwK!~l'
            'Bd&IxLbcPxj++F-'
            'z({Os;LJand=roGW{hlB12TVP#Tru=I@t3#tb+h}(U_IVxR5UlAimPx|s&Ac#JrZjC8I?<H`u-'
            'rs&w`Dcja%1JV~VY#1$>zF@qTs=3%+@+uLoKOHv$OU%mm>ClU7F0ZP_qKiItAFLxM^9zdJuYcsZLj!Mj^3b3yx8%'
            '#f|x`;mK*E?@R-'
            'Okj>?dh)1aYO_?QF}3oS^1%#)77TkWBd*d&lhbjrSb*qdy@eSLLw48mVA%&^GXpB!V(mTRHd3;@q9Tm04BXeLjYB'
            '=q=`AF%vufGW(k5U8i{vS1ij@_5F`6eq=_$5t&T8d<jUJNmX0;M6o{H5zB^`V?t``e%4X_|7PqKVTx8+{au$@_go'
            'p@Cvy&9@ZXl7_6t2ctGP!++LCZ(A4(-ZzVBq(B4%5b+=;-^p-'
            'uuSAC(@VIoB_M@>2q7oZRSH9)UP#_~F`GsDK84?t!`Un>6Qh}XOHXllPo6!GuG_eATUKt|U;#jWVbm}vLzeTWgwj'
            '%MF*7U`x|k$yN!m)c6U}fe1lac;HOp4*q!a19@D6R1fFcmArmbWY0RRm^Ztp-'
            '$5eTZ;Hj>)bKgSBE%gMAeZFvxTLFQ*;$pEuWmWUBz*KxT<v;jsgu`Q9GLAYU*VT-PGW84wGvhh~yVpbuSt1_Yx;$'
            '#0ZaWu46oy4WX)(Jg#?e~10%nar3328+tF99rD=x`*+cbbj8nXMBdzDM2_lw}4~A|2m5z4{?pLe46l>;RECmS#l^'
            '+TJ#m2w}I*>6x)j>Os7qkO?M+`hCOF3t39M+RslyS|?(Zd?XlQ+E5u0)^4{iBYIL=7ji@u=n1>}S$L#qHP{gV<$z'
            '>?+u%Aji>97^ASImNSnlB?aD^UHyqou!%Aj>&AkOjqQHAm?hi-{MxRr4gL|TN-ZltL`OOXaH<Bl}5HmYq}9(hI@$'
            'B4jhZt^(C{T;4Z1ah7s6H?Et7i)I9UX@T==21+xWLZ)63CX|wCS2RovS^!KO)X~M(9lo}V+F_zJy!3>h4qVBJ$`>'
            '$T`q)L8kmQr39uU9-_JThV@)?=t<F~j$+nvdtgzX*?{ypir>5sY$+jQ?qabbA_-+}f-wD8Af2P<21<5g#k-'
            '}xHwo-'
            '~w&;;domm$Y}Kj1+R8tKLyF+8<s5QGcn`(ph5l4_Q!FrV?il;4d1=!W^=OVC)fL>I8r>3A}E?1SAM&h(GtuhO{f%'
            '+xmxb+f~sP!p<BrV=`c4Rxuq^=v5@Pb@XNwzNve$-'
            '(xd@fOYu7pcz}RdOIdat=*LgKZbF<LVK!Q~!>p4(Bw2yJaW1x2a1da?#^)4gmp<MvE0W+3f^-'
            '#@|RpFQunz0*obi+`;f4N@0<9Gt@)_5OqZZ!>vFMe=a~KnnJjb92gTSRk2i-'
            'PC82^`wYX)+b146#wGqQ6c0*o&OIZcAPtkKI-t2jI<67q-'
            'vDqOQ6Eixw>tvDd@Rlrz2!ys4Id`jx#aFliU_0PJ{!B0BBz`-'
            '#4iTorXjrhT!a<AzPjEITTVQ%D;+RJ`F2`Uli0CbR!S$snSQJLy1r)CUO_yvc@_Tv0+@IEo1MP10ySH&I-'
            '^?_s=uP|0sB65z>sie07D@yB6-'
            'ON%wlbuIlox9D&7Lh<>!SXsJX67l1~U!Acd|68}vZ>{BHkT$u&W%d~6DBFK}e)63V`8AmrRHP=<L-'
            '243P4<4lJ<H+KiOmh0v&?dZH|*F?hnMI7d<`Wk#2oQvEfGdnJsZf?O|X?o4wFN;ug^HTzVZvPSHHV;Im#QMr&Q@2'
            'b)cMq+xpGbOmh|%+qj*LG90X|3~0qR>5+C@DkjvzINwl;mmyKup2SYT^=N~EJ8J>y7|T!C4NaygX?cto;Tcm|Gbk'
            '12zOZ}6qEztdt($^I6jcch~rw&YtAZLWl_RZ3rNv^kqpAzd~<hLFs)rBZTalihSyU*=%h6ckG=!O8Y(DW1Aks<($'
            'KWQzo1vAlix&+j5R=^gIeAsEcc)akv6m;YmS&SCop6yw7+5J@6i*GiEJp8*cn9QXm31C@;4WrJZt@09A&+Pg~S2X'
            '?|Zu|BWdS(OqQPlNg#KrZQeR>sV}rGh1456FFD?f5z{^nWvOMZPTPGkRm=8CDZiX4=dcOoToeNA|V#+0+z$bACFK'
            'TX{o_*rZHDF{QPrAk&m)b8u@B<-6ZobN&7K?^bu6H50RLutjOziV^Xpz<XnsxKfS~x%x-}q4-'
            'AO5pLNi6;1A9^_IKbrCE3O;Jpyq5=82n<{T${$U^4|frBKMpGdrxU+dY#Yy^KA4Z4}{G}E^PS$o>@YHAC`-'
            'AUHwi!6dg*H#Lx_mW5Mtl-'
            'Z3tTXa%$Q|bQz@MMxTWF19c6I`uhwl$!GtXMbF_f|GxY;sL)biHJT7EC%6J2p}6I2Jwkr66CtQM4h5Z=*8qjaKiO'
            'EHgFx~)f7OOoM7j1))FHlzeA<>Heep-r1vX>6BamnX}_-'
            'NK07tzgG*hknQUVLc3tJp%4hV!?a_d}gIKH*>XuhYBB__^D>^jpCr(7%#42i%U9vJ^kz^Q`+$|Hh1Z|SV8dJ&O4+'
            'p@tG6i-'
            'Fi$qSs250Z#$zpDnbU01is<VSj*n7R=}?Akq#oF5)B=RkZHAj;vxN?sT*HBZC#e<rMIsgDZsZ~GeMH?q8)s8;wI6'
            '`pjl97tS1yH6~#rE-'
            'W{ua``hpF)n;Kdrw2(9U@9(Y3skz<;fduS(Ko%|(VQtxKP$t+s)9J+3qD%xbvw{#a!#VD923ep890voP}s|=1s4b'
            'y+pKJ+L&|0v7#^OyQ~mG$mqUm}O9$I?wpf@Mb>Rz;k<+XiZ$Yq2$5RR(FYyw%Ss2I=3zU5vj)l5D6~cEvOMWMmRG'
            '5AmFlOta6#(3Rg3_mc*;ay*on4}e2fh7M5tqTBb|Ei6#^t{V?6VS>fncJfD4~U06MvO`D821An)^E|AzqmiOCJdo'
            'K?#wB*X%b{KwKesn+V)mBgCk(VOfDgfF3|P|6dmNV>?Jjf+`0XxOb4u0_nyk)e0Yu!bYO)TI1DeV9?=K$-'
            '?P6oWB?Uh6iL|$vi;YGUXJ`>-PtN(5io!0L{UxrlS*c5~-!6@uxl{u-'
            'tb$FdGg$`;lc&{UqWe7C!^kDeoLDUnT63@09~NtL=KPg!Uy?L*%W;?3SX{exOl46=bqmffX@L9TA$|!sDX@>s@?5'
            '{3aEwbl}S*!1&j;P}s<mr1WXA7?-oaFM*t7aP&MTk_|dsrCD&j?o;j5yJsofH{I5~<-'
            'N7>XB^7QY5@r}pKVse?)LpC0Nz8+_uCKD70v8uCLd9wkRe`8LvSeCi*nMBy!pBiN9}z$%!{*$>f>P5;SCs;_2My9'
            'H6CFyRTRgXoR`VU54(<4-|gR;XtaIEKECcUpxG{I?2Of5=JdWf%xCa1fdMSH>y$!eV<F^RgpsyN-~IdH-oF)lf7{'
            '>t<1pVle*nJzJe9O!tE>JJIXQnSx^nG8wo63r4Hll<3+iFgZ!0>UyL&m>|7vn)E;L$3*~iG8A;%1ti_0z>7rY5Sw'
            '`u7fhLw96Skew)?jM4sbR;hM$$wjhh<q8l$+w4*D&fFL2Q!2R{=k!Bc_(cG>>A6kgQya`J=^x{B+R1*pSDp0yY7{'
            '|^vM|222Q5JFlYv2Uw&CcJ%w=+AWNH#j%<gEA}FgoIB?P_Y;pTe`3a7;?0NS=;LODMh=rFTxwWVqY^j>M?$S<Tq8'
            '8&?>&pAWU7V_@?lwK;iZ()@`+*$;5^*CR#D_9tD7P9ppR|x(7w*MB#({J?^#|J+fR4qZT1^M$u2W97v@7dylQnZ;'
            'iH<UqFDHZrk4|}SB`kcH^qF7Sm}Z90_SnV-'
            '>f+I6D<Ol?ycSfMi(6!UW9h*C7Ow3oMy_V0A2CdL1RlWEq@BOB4!nT62>OWM8DOV?_kq~7Nv_M4X6{eW$%(UZHQJ'
            'cR6O0Uur^u;7S7i{9@yI>F4>n^EPp6yN>_%TcFmW;qQl>efe!#urV5$?_{2UemPj{n<CO}cq6K+%87IO~RK{3;@%'
            'tKj@i;X}KJqA?;PUf2?rh%jw@d(MFK0vLtN<MkrGm$!k;nK)lG*R8(Sq&`9vNuEy+kKBhSO4vnl3y_+ZQPt=o3gj'
            '2yKY*liL^z>nw38e(iYqNRzu%Ek<kp&QN*0iEGq(CK9yO%yPp308rR14d^sx-'
            'DPh<1Q$B^Lyqmk4-8t*RW7%)An7Aw!7%>2NW-V3%n=Eojr{F9BJV;_iq-ho(LQxpfgU@4--foO;cja^yZMJL|k{^'
            'VOFjJ<4@dWM(<Tw_SsfwAIx*HMR$_w?FTWGAaS0Unqvt(ABAYTCi>eiDQw1xoKp2?64h@-'
            '%N15c3WM({ClFUNx8gWFzX#QVjgKX<MM$WeE5&Zjyz?qN0P%&*&dc9?H76?SuUY;$(R75)%k{!inmh%liaC}>)2$'
            'AI2~;lFHWMkq6V&=kB2!7HLSra;+OcoyA<%|3%4B`V>3qVvQ_bBnL0{u%ryz$S&1vVzcYGg;<u<`vn+!(mW_8?NR'
            ')al5xm!c*n%<%y7Q4kjv!AoBFdh?b5OMByhe$bVzUNZ%6?VcmU4LhQSX)EOCZ)QcOC)S|7-'
            '9bt<?)0C@q;1OsqYP~bx;84F9!%@31igJ7&zvceyU|S2ibd>XkX%w9{VUNq!i}~|;7k2Y9+}qpG)$7oHvF>gW?`R'
            '!wx0EZU0=Dk71Arav;oTO#qabw;H;m_wQ40^dQPx+hdUJWz2_@2_g2}zV;{bsKi<g1yKNmOpHt$L|+UV|WX}^f#C'
            'ggi!*2k(6S(q=urjpt1iAu)aj*2vdM^(W|D7*Fhs7<pSmAj!aj>68Kon5^<j)#Y?ly;^<z8<<WS{q7-'
            '5C6Bl@s2K)tb-'
            '!)S^OhG+eSyH$bW91h$)_gMU$|B_rH88|K&^h489b?)IZdXg8q`o4*i!K<v*_*<=$?P|KGAMyQ1n={uMbB8X><G|'
            'JvCB^mk%eo{dx?w4-P1R&Uh(y;i%BXLr*4G_njC|D)u1-'
            '&?eu+;$)}CbM>zS)0@9lN^WLy@k>qN5x4=g5T9IXp!9C*AItA=YMK9oK9KeIo)DIIzBe8OO@AL(n^=vYt8SVQY5K'
            'jlii<98@2N8m-|T0S*Kl-iHvf=1@4^%>9<IH)a5O*lMyM~CDJo}E0HNTkl#V_GWS9i$`;Xd5IRYYoeYT0#?eUg`y'
            '>Low|FBH?)-fC_SNyLA4Z13iYY@Q!(YCB`|q3tREKdR+0$IYzp;{O+k5P`1LQ0b;0=p0tWd@xavq>a;Yw9|n-'
            'Z&|_Z4!jsw%Bbzc5S0`cq9)Ng?D$qY5d2!g`e`FhaeULK7-'
            'ak3P3#QC_PfqD!KxDNs#SF!qCcQxoT9DK;JCW20bck{`c1Jvn-M_WEu9_UMP>)3djK&JWMd-X4Gd<Jr+5d3T-'
            '}^?d0e4-JE_b(|sf9(c?`HuX#!9jU8@vKVuEI)*SR(P)wuiX>*GUx!i1qUu-mbuJ6ldYd`m(zTJD{U30tg1DhKvY'
            '1s^#X^}Bmx2z(gdw4$X~$3M3t$g=V^`&+XogZ4Zs<MtF|&Y48z8NMerxUlSi<8&L-'
            '!VndR(RW%iJiu9X_xe>fsUWrxLBr%EZ0M)rJM-@{prY?${wMz(S4YE4xpJ!AcC#d-'
            '{nu`m6fJC^TcCEi>B!CHAc^tD+K2$Nq*da|Ej=kF%m<&~31Ax>4uZs2j^k8l7EHTPA+asSLaNWK?1Qb)9n=YtfF&'
            'RM)E<i<RfU8aU#ahO4M+DBLQ}Qgu_aRySkz3%+0L>jhOS<pQdF-'
            'y)ZV&#J;SmQ=sEp}gK|lpz(ErxMU84)n~D+Th)TkA&~?guYrOwgGA5s~Q#|KlPPtqwqMCzp29qtA)<WfT3gFPWe}'
            '(Za29ZL8{WimaO^*0wQ%F;N8kKqX)qiy`a~kSPB|k2c$Z^F0MvOC7<iXw7LW}TLsFXdckuVE;jRva`k$8BH<mg>y'
            'jq{DVbdmzl&t`3`k)5l2C=`1)dt<tzx>9&Dcx2<tjx|9U3IpSC9^i2#aK>Cb@MdcjuO?6*oIl7?2xPN#bjKRdUwS'
            'g?&31LYS<zZLe#Zz83sCe7WJhtccI9#ViE8kukaWLh(Co;vLb6me4>kObt1}y4{(n9<<k~x5V^8FC_Nc85@FS8A2'
            'r){FJFSAa&jxVSW&}Bb-Y=%x>h>pY=lWON$KDRXK|5L79)st-4N&o-'
            '>GJr(HmkD~SqfzF|h4Nn0u+yFBE?s|9^49v#pULRJaIq%6lcIVY6*i_gFGbfcyUyi~=lSwR7MI0<<U_N+9|;SSAn'
            'PP~E_YS#O|OG3zu'
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
