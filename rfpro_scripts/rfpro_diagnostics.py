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
        '0741864b5eab76e10bbb1bb52ddb019b87681909500bf3aa903bf1d40b0e6868',
        (
            'c-'
            'rl~?RFbSk|6pYPf=Zc&o;^eAxdrcPD7^W(h}w7S$$9>ZEugvsV)KqvRVKNMggMO9G<feai3uyY@cK^KJq)WP@v`R'
            'o_l8Q-L_cBjLeLTjEt|0NYnIqu`XA|cwK!gXSd06Rer3>o8+pj=jD2Jn-'
            'q&l(i9)dN%FdEt{<P&t96q!H)Xj@R%Nr9iNC5va{BUQRS$c;)6F7TUss~VcvUUe;-'
            '{vXl;TsF)XS3Fi9zbWmgDs>IbJ8_r==L8!6r>P6Q9dTuUHhb+oo!M*CdMqW|sWrFUw+8h$)q;v-'
            '0OnxfqwtU;Z*kisf=vl}%DF%4Atri*-_n|36t*b1`ZSP<ymCIp_dav?`}!_Sd2#&Pa@-'
            '77WWDCNJw%($q6p_qbk6s&!Q_#7ft_aj{5>SyLyox|kp=u>ye<1;|4dp^4$XsgtIfZ)ODo>=mmr8L!GhEP9ZLWo_'
            'WU6M+W&Am&hu6|8QmrcCDbq?%UcL}2+G(7CFvDuE`su04gHWLmFageC##V)S*r5;MBFE*FSpu_sH>p<eaIv$`ppV'
            'FK`Y!^GItrJ#p35W}Pv2wK!@Tod+{JJ(CowAY)i>Uomq)6IIbD)T(4=7@=6A^PwFd-'
            'B`rN=&dR<=@xq`Aq)15|dun^{kN}=EeG2{<~IRSE_TfxfBx-'
            '6rg@<Zq+|w>uF|_VqJ^{9>f~u)YK<xu@nP|^~zsQU|jrReY>m{SMvMe;&vctRiNc^Rt}Qag6PDrgG5qduh;u+awL'
            'd^Xdf{x$pKEp8R2$Z&*wleV?>Y`yn!vc+RV$vx*7If9KAgJ{?&PY_~!7{pU;lZ@;8UCkCKB#U|Rn4Z*Ske&d=ZGN'
            'B{Hu=*{_=`0=Hn#Zrv^W-}MtmekW^BIrU;T`>hxfIXX(<7y6sg2zJ;M{@Gwr9tn-Y*XSP-putRPLEFBo}T9?ho@o'
            '^=SQdci=*equMc14C$A2lAHm4K@8!pD&Q6Y=pT9j7&A&T7J3sw%et3R<di?G8=Q#0vH5L1mBe%%qfVrZ-MvzeN|5'
            'aPk7nuKBxi~mqZOW{NpOQ1^`UA{x)Jw$w39@@DPI?KGhC?IS12H6A3Z6;8z@{lzd(&bJ8@Vb4V`~JSkt~Nuy#P-'
            'gntUPtJ4%}M3cn+y5o|pEIjNfEthlA$JI(n7kZsQy8J(E2KB$5qE~^DjDM7LWE+$vRv}Mc{Knm<l%1<M)U2FU(o4'
            'MZ&(C$yP;iF`|S<cG$8pDHRI2>MVUEaI3AZa*cdUcn;6B<PPq$;i!b+fL<P4b}>L|@EcH9&Phi(*<!U~YU7h&y5B'
            '><BXSF@DteU*5tsl25Cd*c3da_;t1sEYSFx{D<JLi_(RY-xN*GTy~UP3QmJ9%EiZORWIQ5VGGGAxyd#>e8=>BS^|'
            '$aDXwf1MT*>`Gq=JfV&ktgb=FImnmCqpeF(ZBl!&8x<!<`Opeeb970=UL^IUL5n1>=`1eODr^AR*ImdLit)v8`$7'
            'veQYRpOj%ntWDVmNVn0Z76|D5AVEFyz*>(;I&9=<Qq|<LY%H~{jprx*Cvdl@t`lw99AwDXnd|W>*Z!`(2P80iqz?'
            'UMb`oJzhHW2#9ikf#5tkG+9<t_P}pWsd@QON+zEnqiUtUFcT^oOJ_-'
            'V?SGNjVXT?<9_H@T2m*rY){Q`uLX?3*$91*WW!e|Wf%tUQtoF^8gJp6FW{PH$uA~UfhJ`CLbv@ljRjhJ7qm{K*?J'
            'Ow*@O%atH+HV%({vThLlbog~He9vD%~LH6X5%-Y7Uh%|nhO?0qxXfFIURWHG)wlraaYXSO<M#12YgIi-'
            ';+vgF7w=hBxiAh0_35GSk)Vk<kSU_92{7av6|CPiG#Y}VS3J2BuBMYlOk~zxL90T$K4&d17MH7HL1QaUAg?sY5{l'
            '(G>YQLMG^fzRHrYgNDzh9vH-6ez`->eC}5d5hJck^@K{tV@}JkaxX9NaA?I{`^bt9NY-'
            'r(PY#~byWuu|sgaSi1)%v=h&Z@=cQ<`}g5<gu2{AqkSZ0a-w1U5LmsTRL~n)-cz7C%htn`Stf&EmZ$g-'
            '`+(X?W;yJ+6!4<W~HfAgl^d82Fk#0{-'
            '5grr$4`&62O0cj7W)@T26;9PK_;NSoDTpwR%zyz3Zo2>(z_?6CO&qaYn%r({*v>t+B_0MJ0O8egMCz}ng2i?hc^u'
            'aSd6JI%jPE;_kA69fKX_-'
            '_4N+|W`ie+PdY>U(~Wyn9t$u8P&|@nTx{Oc?>BJHeRS34wXa3Wd`O*wd_P*6(3m7ozifgQpaeNiJL7_Vopeh_G44'
            'TC#S%b*xw(p#Cu=!4Ra?em3ME`}#PQpT;0Zy*<N?bU^_X^z4H}z~L|mteeZRx*9(W#a&Y_CVkmAv)9QegnemWsgI'
            'P*oEk0`H{v&fq9yj5)Sj0QBzbJM=E>py!Mqw2Zv-yQy&uB2zV(Iw4O1VUP|p)JLoquCpuH*+1<<SSw9a@|K<+adh'
            '^8fWz@^gROwXk08{9-p!tCp##hZoMTuy<{CNu&9(<fEnWK}Y!b&zayL0sd)QWx)AJHA_|ZT%I7Ou-xJL13w$zB|v'
            '~og9LGdH(Y4>1*+i@4q{KBQ((SKc#~Nem1{k_MI$12~}3Wshc5#A6}K~zB`lvlx9Pr%vI~YXbOmH%4OzV(Fo7KiG'
            '#a<ZA}VL2#Ov+Lvs<Eq}x9>`IU8cbcdmk<>0^lEW``UmOP_kHoGjwA8^JE@G)cC26&eHcmu4;Y4s^1$*TNRjyG!%'
            'Bt!?*M1OS|6)d{|o19n%tXj8ZvTH0lmrao!3}^KX@IJig&<^CV1bYRNTPYYcfGvMq3W59sez{(jVy07|TCo&|Jkm'
            'd%937p#eVM;FK1~%XFuE927Muj4#%P}rka7-'
            'okLwyQ9d}G|&7Hpe)7#fadPLp6(}23UBs;oLL1c!;{>3Ht2#>1R9~*dw%Stj7_|Gr7v4kG87Gjh|+;CM{;{b^ZWD'
            '1giDO)qB7VcWx!P|}9n-0Hb@zn#$P#J-'
            '7?J2IVX7y#?IIfw`F2vffckIYIM;F`fhDFlkugmcVlqW#_k$0v!HIl>lLNYkgh1p+h>l%<VO~vn<RU^bQAsoVD?^'
            'BC-Y@D*#RIY{Q0qiCHX(1%Q;a`PV-'
            ')G1fYCSy5awcTcw7;myiXmk|f)$lt^|43|;Z@3(cgA9Wv${`i3epCq^+u=$#b#X#+=}~mHoG1Ev`7tLELn<$8dv5'
            '0Pm42N;|NxB$E&+H`=(&oC98S!m^D$5mWRvR1oQ=zZp%+XzLl08aI^?6EB<##V3eqhm;hlLRSYF&yY?+d=HjEXtG'
            '?3nNS&3l1H-UBTx}M%()T`{O(rRtPRyBQ7XzC#VVe)oEbaWj_9n7JpfSX5uom>^d}eNHorFZ}ZD}8gpuY3G-'
            'pr&Jj0R`YdMtXu%@%u)@Pz6^+6Ml`rU*k=f3L<9h%E)C#nu~Kk7U0ENi(dTHtUI4Zt^J6e+%F&fI#D>Z;8mMBH9$'
            'dKnwi&LhiSokY0WG=;@YO8=h=-'
            'm%fu{#=_7bx!eGY{&`b@0gA*<@VbG6iOoCqK}kIwob0c8y~<bR1`dj0pd}sLH!Pn*OFBJ!_00kmSM-VzFg|_iCpv'
            'b8_*^ebFcA=^)4HTZ^wQ@;48SC`Bm55-<vWp@g+j?t1dEpBcPSNC!D18FK}u7c-'
            '6|()k~&)=mW%5GOX;Q9nwePI$?f`DOwZsb103qkmeK?(92z@eQg=wV{;`?}0Y&-B-'
            'Wf_u&o#qKu~7ET@oS#D@_@0+pre_3kT{lW5aRku3^E%V_8iaZp(v$anA*QFy#aO{kb7*9kma@Ki{9Og95li0T$+d'
            '2$%Z6--nq8-coL(d8l|Mgu-'
            'L31T^ArVp`%K`0N+601@z+hOaS?Fih`B<<Bx}bes%cfMXnlUu8?MqfQDyp?re3qOY7-WP<UA`V6yXS0UpTo-jOZ0'
            'oFzO@Z|a061ao%g2vnj>p2&f(R>krfZh8($aE=p#d{t}~LgGN`FN_|Ixc3AhJ+lv}^nnZL<1$g}0)Kotw4w9<e-'
            'zA-Ri{?178`@-'
            'sVU*|RoyH#mWURjGU`p^(}wIsd!>JTFMj|9z`3$5jmhGP@zdIWf5Dm_1Rcz7Ep?99VDD~ZE@~;D)vA9R)?JbhHDc'
            'lK806uyUMdvOndd!FVGjq1CaM_j&;oDFOYR9yMQsbywzD-'
            '^Z%4*tYy>f;ftswmE0xa%<k_arK^N${!J87bJ8)r*%)wFk*W$jktjLfJ0$Mgh0-'
            '9a$U}8fjxg60NYmg|XI1Vd5(SQg+U^YC@%oI-Xm)7euJ=a!XD?A9boI>0Z0#Kr6ua#z;oW-JG#k@<-xO!}Kbw`-'
            'ZG(F@MC3jMlQ0Kq=B(OeA4i&qRQyK+$%%cSO9!X+2mCRujuGPlbr1##gp&x~|S4o4jQbGp`elpq$b^oH*j*0Y4kb'
            'O811vSW~N%r>Swr@j51PMy(8DH0+GDT<)#7%K7#O?CSsL+N3%P`RPbqH<26X8xM>m))QFNCi1qAF(fl{D1Ql{pY3'
            '4^k#_D6<)GrsH)v*L#AJjG=bo8Nq-'
            '66@!o*%b1$fXeo(#WPHSR>p%DPKMj@5I>B<D?T1($99ke;AfSYgLBN{{kyW1Cb`%2#lNicO?RZn>pdR*hT#oIwLu'
            'COW7ZAJv6e$H2(9;%IY@tlZ$5eiTa3HwsfgTo{dAX{_6c}T8o+yk??2p)zVlAfjk-'
            '}tB{w0++j`Hiy@G$iG_pH^fhO>nQbL)QQS<sXsV)un(*mHp3)U>}-'
            '#z%4N6@~ot@ek)35r6PC!hv9Vx!7DRS4C1F$7tMT%K);Fz^((e4sbY{XJbj0s!b3>>Q~wnF}FNAQStXl`&`u)X*k'
            '9%nSdqEtf^LwQd;O|B-yYb{ynw0*oF(BKq*}9h!Jx%d7VoEJ+|`$1G)-eL@Ef07UD3RtjcM*N-'
            '%zI1(pyMUaBHWFCm^ooG}Pxf?!MWZ4Tiv^ULaLBV?-Ctv*%1>IQnpjFEvj4{mDvNi(}!kp(s_sAeH@;CotO-My<_'
            'vQfYc%9&MDV=lpyW=&UP7zs^%&q6bEd*KA_DaU8)F=rA!DH0Qn%{K6h-Y&h>3?y}v=ONc&n=<|p0$tW?L4=LN-'
            '*n`hCg~%DBA}Pz>U82Q!KhMGth0*K<X9`Zd2g!OELm-gkVU>IQR9}g80v6!n848jh}J}8=n_@5PcdE?fsEmC*jWW'
            'p${SKiK11nUrHPKbmD^4rJ7#oXE<GvnG88BetwiG5G+!W>5nCfve2n<!!HsAvb<GSkceya8L}F1%)_c)k42*3+aT'
            'QvcZDFP0H*`YKWNgypIFCm16g~MjD6=`_FEx|^eY+y^G?mLw?ra1KIrqsu*hWCU*en2^5#%ccA6HMoC8$MjA3x|g'
            '+BT_GxhxAoxtf%vUNiJ{7JHt0a>HUWA;rULU|wgf0!I+*kt^=AEqxGJ^8h!A98ViiCAXl!<o+$!s&S(_D0I(;bU*'
            'ef6hU<x=%J)T*YxjrN36vcNG_O~qAT&ZxyKP@fY2F~MuYIgkYKmWgvOPt^sxIrxRHzumaWxz?{P0Lvhe0(lmRj?e'
            'OD;X71<8$NOA0SDzMXynIBjY`qmig&B{<HFO$u9-'
            'T#7@pE<Xsx{3pVl<<E#0Kad)MmR7Kb6}(AfdA_+P;a8$17>e5rWdDrx<jIysBe|<xiq3a4?u_@aM>W(*gm)i&czh'
            '$;%(A_ziq*ev=0X?w{JQ6nRT=CwYt@c<z38{32SNJ?h?_qVoV=d+7a!R>)fV_rY|pf`5?)>=v&N#4SJyZcckUoKy'
            '|z>S`10tu_Q74HYDWTOFgq$6wBtiHm4|+gMcB?oHEP~=Q^pzYsHs%!a8yv?Zsrn(jUpMq%2Pdg8zpNpQ?v6dEPTV'
            '*p4H`W5YJZ&P)&?2wfn7s19PrdSIoJNC#-'
            'I+Xa@A>Bd;3;YB5Tk`WiH(3o20G;W?bo^symJF=J=2#_`gA4_U+_tN;hT+ZY*x76p{-'
            'p|WI(0a8f)qanhog4&St~lWfXtMz`yHM$f)J>!aAzTi^LBlvPd?IC>_`p-'
            'H7OK(QQ5tsy2E4Tl1#_QUp_v9I#e`oP$W)MY9GoE`xF=^DM5C*7LI)<;p=Ir1@4@y%xOLNl8w9YCB9-'
            '3HksOocvYcW#wthjZ<a0DfTKn^0+<RNuvIlGfA)QV?IovGKZ_9RyfJcSoBgB&CL$rQyX5;$T#p<fm54BF7mx68yG'
            'R0OgI>y(<;)+d<v?hfEcrz^Ir>44E<QBb3Lx{U-'
            'ao}_4^tMpCVe?Y3h!+UsOdy#JB);8NSxUl#W;?_*L_IWya|A3uh^E6AXUWt3r+-'
            'Lj$UUG0$3vnmiii>MpDl~*XG1HZ1aVp1LTru3okkh`WSNebB6z!WCu$04rk`j`JrCFZWMS3<`il_CiwWUVksT47d'
            'bjJKlqMlC8D2-9A1&+WZ#GJe+apXb0~>|PhqGCMFWF~4IoaKt(Cy(!G>%-'
            '*a|8p+8hKh46Pp{YuZuMqWiCrJjSEzX%R|1uX3R2rJnMcg=5bw5d@>rEOOILnEo!hK{wn87?dL1-'
            'MJmUEe>iBl7K3M#%H6%ijV(dRHAZL;h~cN;^^qvyg@|yYEuPmYd$D{SUD{E~`Eq?Lp_w)mUfFwS59{G3=8nk4#|5'
            '(VaGlJ`qFJLjL32?DOHZn5RM49vrt=Unkttu->hk%#;!{XohBu?-'
            '+Dw4~u{oQ|d9}u<F@02OQ?!hoj85ktOd=g`*{lVs5hZ5JoQj!ysAAM)CY{4<wsWF5OzV!I$Ik+!wctJvWeeKOcAI'
            'o0ry`hz1t&$%b>I4y-ES4$axioMA`)t)7b(|CC`Qf@d|Y`|F3`>a^ir*uV)mF~<h1^wB(q)WjqdY*a-'
            'vbl!+6AMeH#;Jjr0KCElN*&!OO9^oK<6$MaE1Eg1}{PI6C{3@@x9@xPw-'
            '@<R{|E4b9WIVdd{))m8HY{MdT0N(lbLTUr_4CGK6RsFcU(XK>eHXy2*?<}ai7ET^HID>`%J$kH|6B|eyD#&M_9^g'
            '9oq7$Bca1tP%%D?`r>XL>d9z)_f(1}4^k4Tq_Wc7yZ-'
            'zAR&4nwtE0eS5t47(%&1w*{*`gaI0|aA5VKhdcPv&Iyw5fI$ni8OC2<f+<aGqCuLJb-_ZS9WSULaYUiLKm039R;E'
            'u_V)6+dL{m3J?*i{DxDQ~SSvY2r(ku<~Jn;*yc|F<8N@m!9tLr()1^CJa?00xPIfIX{d7oX^H_VKe1zhS<pyk`!&'
            'R3<aAan+C76Q0AkKxs(8dC2QYV`w5HS_un8!@(|HKUCOjNghJK?V!Smn}SKra*wNe4tkQA@Rdq#}wr2VpkD>4Ii4'
            'BD?6``sDnwP+lG{?k2o>#o&k+9Mr0Bs@R}Bo{{;Tx$N@WaO)4^F1?jy6QN3I5HS611neY)dgOzSpV2g(c3`m!=zO'
            '@|BY-Vc0f$}_&(2F1Zou-~y=b!!X9Q!)sw{-'
            'D131=uq4s#&D5C39eNQLz6fGkM7CO}q~8zD=`^9V>Ot_tu}3p8@(G!DqylbA#H5P1f|(|1C=$gIRuvzUM1)Z+%pD'
            'FnxW&jSC>wxQ+cbzWn(q+H!CPDmSY1^1p7cQ4b)*>!bUe-'
            'JmZTw1dR&9}Z;2*#lHFnRvyQ9|RiKYnQ#ob~+W7=Jqo-fM6X^>hlN0-'
            'pOCVLTFC$D3WjFaru0M!vpXmJ!$z3l{KglR|*MU}7c)VpN1ugX+vj$s(U~F$o8?zfB+u3+|f`1v#gWee`S2u(c>l'
            '^`=OX0<5bUM(6o3x~05wOtl4?aw$xQ{v8OxG=dQoFo#EmxB|fw`vTC@44<};^k4@IFND-B5c{`sVoeABN5=-'
            'M$uN7!=ZkV)FCZBii7C(=o+vG6#klOJ|Bav0s1N_=fBkRxl-SySD%~!tatM*DVp087`o7rv+y34kFCK{=-'
            'gv{Y5HP3p3}i>O25=e+5oxjEB{Vto%i;aniVbD(EAdEr&;dW?^fZ5DTB#vb54>&22BhaH3!2f!X?~&Q|36oy5UOC'
            'TglCeh>nmb1>g_5MA6wWyfL$L0`!J)MA#s!x{CAMN?*qhvHR<G0LSHiuTgSK(_`;Ds9G;{jeQvJdX%<7(bjg|;Lq'
            '{JEHNiI^mK}<l%3BerN$^?znyJVen#8u}<FX+}!5Colh!TSbF1cHvL$t5flrjvUe<LCzqu5X@NP$|yBDjx}Cxp(1'
            'LK6Q&>;fM&+s}QAgdoqL)!7bZ*<2#Ew68I?PIbls2CUJFrS!e;@PLj7jK(?|q^H7axRbLGSiJnjIE>sz+`}aW=Xt'
            'D6U&Y*_W%;ekt{RU2ON}^)U3g=uy3<p}f&cUfuO4pau5nxlZn>(iuF6%*A{mgn1lzeaflD)_QPrm#KI+9eb%!O{Y'
            '+myA$ZRbY=@4`oHc}-'
            'G7_;9U(&=bsU<L+Hz~!xwi{`~*Q_P6pjc3*PgBQCQ63l4qUF`T$MN^N)k0>?pF{EKslY@5=Qc#s1)V1r*q36Tmnq'
            'NyydF~qi1&FfKPI;O>|6=L*g!U|yGC*$&orK+X*c{k|)MjBY+x1CLb}b13dCKb<Tupn93Gm2}MS%J3T|fxRz+WL_'
            '-WRpn5YpkC91r;7h4SH2#?PFRa}ub&r-'
            'U0qfSVF^ATwaeDG3~mPz=N{TQ>QzF2(YJAq$|^<;n)?P`!j?dXkVqMNYo4$(Ru$6|idYvHpOO%7(77D#!I|V#fkw'
            '&cXNuj9^5a4|JqsnVbY{Gy(}zDxYGbx6qNJw#rhvSyOLTV^&VpM=<{8VpgjXb44=$^;4kf8(Ik};-'
            '>B*_?Z*8MJRpjM_#@RIEMkkbZ=9XlD+Fw<5}LI)AWv(4@ohg)4dbDtfg?Y=Er4nZwe_<eX1U4YDggM<6#K==+D}d'
            '(RO9yU6!xJETN6fR%J1{l`K1gn5{F5Ud5ee772lNr^}he&1*xxP=tgLYVKR2AES%G69Cq6bsRvr`f8t6sY&BNZg;'
            '}_iq@q4ECB4$LGl#)M+GvrMeRElV&pJd^aEf6b@mL@d?ObvPoxa7w(b6c)8#DUS|&^Q)=%M|X=f*Z3Ct38LnKGn4'
            '02lRVx$!|GSet~p8_38kkQT-t=SEdzPZ#vrhF-'
            'CHUeqC-{0@~VX^k@;~OCTR9f~!+3z-$&NDLBDMsY~Iq(lut8NdsyzXinf^+u~iHe`pu)>NeF0)?dv+`p(dx-'
            'jH<p@Xxs8;}qpAdIY1=Zl_*itjGF+u5N^L4eJ$(J#{&bCFTi!DHnIl%n3Vw`grhO9Upc#JmlgxlbxbL-'
            'AAmt)vi0^KC9@|W{;Ka{C0Md1wdE_vg^MA0n}{MmyR;8&SV-oH)wStY10m?3{&REs@Y9r1z7Vl_;@U(BixB|R(>9'
            '9it1Xy%OgTa+!IUstoqs)Srhlu>O!zD|LkS$#vIoRH|GZ3I~%geq2xp(lUjVr(hAp+srD6ERyo&>&zE4uJZ$SamZ'
            'CsBv5E0%{GC%gPT9orF?+Zh6rEnr3Uiglc6)@PD!!Ga}eC656XPK}O~KqJba>$Wl6(iz~v$HEIrH-rk7fWg^t12L'
            'JJy4p%e5W@vO)(`?0V5N%#^bj&ho4$+s;BS{e5<mgfs)C3vr7Tj|M$mcuTH_UowA5Q+RNwIZ~kk>HpW+H4g6?)@F'
            't%k8H!(4_jtAulN=Rtd-wTzI)VRQ|@)vDsgdj&MZl+Y+-'
            '#dkR<k?NFuAIsd7ySgAchHPU^ZAQ!Z#ir6ZTa)sHq@7mSMYM}!WDsp<@{SOdnHwC3f~f=f`noeOX|RzP;$#%Sm;3'
            'udmoTpGK?K*%-FI4IR0yUaSV2jySzUkFER%XMy9Lp_z?w5c$hxd%5Hlh(-@-'
            '9)L80t>xe@#dk{dt}5!}jhS#E$4UtIlc7*hBme72)L8_qthxQNYIZFx4^@oox^-'
            '@(%$(;#RyO*&Ru8A+7J&92hf!jQAjz&q>vt)q7}ru+gU$mceMw5}(lX~s`zi&5ht_KWs?X1V<7en+#xldtw8Kpq{'
            'K3?nr4xKSZIYX$eoelN^`n^u!doE^9DG<~)o$X~UIqZ5~JW#(Bg!g5ujZZhp|Nk6OU@BQAF`=bl;=`U*A>3ky^Bp'
            '<7$5<8Rb?q><wrOnjO!{mjoErlaPENzLoYHh{ykz9xOCWba0o`d#3l(z@7VtzR(`1^?e`+oldf(gYqP03}RBp1yc'
            '%haT##FCDQ*hA~C94>U=pDS7VvK-'
            'T653U?`XH3IA^|2J~UC&bcOpJskJ5GcBlP!qs?Ld!Poj~akriU?#laYK7BRUx}iUlBefi|7lGzN|#SyAt-'
            '_*hc<w?ocVE^lgx1l{1n*CK(Gk@#kZ-'
            '*I47&IxwI>Z;`KH0P&1GU!~*A#X#T_s!(9(?KZvr|UYwoZUttIsFr04kBNg66&Njqhva(3%E-EWw;-'
            'Ale84|ITrwh*!gbV>!^}HujiNbxAiB{=cT|9;Sp;AElMcLDgJq~X|BKBtk<TM5$jOd2~Ul`>}JOLA*MqAwXGBa_I'
            '6MNsUYkx!NG2d%Ixyw>2Ti%yHe&+M4R1UB2G{axwiQo0g+0R>nKXsI`(coG;+Qk%67xU!~BH+_I*>nK~RKamshHR'
            'F%>k8rsk)&#%{Y5Ta#bn-'
            'l(?5c3Exl`9&$VRJD|QY`25=;dOple^TuvjRY{LkQdsv6}&aZ3d!Pd_n&?hY{I)KhFvTKqsEeJ!+crKW=?ZV1PyW'
            '`oR58XKTWJb23jLQBt_#zTT{#2Ol;7tM*}4eHnSais3!&~2?IQ08trJt^~RyAOw#bN@!Y=Ae!6tdfoV$i+5y`H*i'
            ';U(D|9t0qkCYW@um?>+uFLxM@S48K`XbH>^#>gpaYG8xF$KhbPoJnUs6^+dAQpb=P&{gzjBpcOu|?91(K^SAm})F'
            '#J*dcM8(@Wd=*1Go3&ylUeK;sdRIWAX&jCf+G5R)tefgbYd}YM>4GK<wF+pE=8*kv960N>W#HN!o=kNgXFEVo!+9'
            '-EFT|-vcph$iW>P}Ej1hv>&ke=I{8igfI*Kp*7m$NX5^cNwaCCE2lERcxl2jv1g(W-ksY>S(Jjz;Sswc%v3VI-Fk'
            '^#zKx-'
            '1&I)jUu@R6P3NZtKNy|I8~tp>84YP!zKO5c95z0^p#i_#Ei>K!24~39p6#0Q>F``mhf}T@!)s>bGD|b9BM|+lDtT'
            'i6AJxegYuO+bP(UZVX8R@^)cJ@#`lJNvRTo>TNLYtrUQPR}x6U+*4gqqOBz2gK#MrrHZi9FKJz$6(=b%YJ$qz9ra'
            '1_qqugne+ws}{;%Pnk$NH7$-u2BYp@m`H0mtV^Hw$Mu*U<!2ih)ICvHGZd`tAe4YqF!9e_#*)QGK-'
            '#zy#NWN)$5*GqM;8ye(5%KW9I2QJZUNRU1sjYc#$c$BD{uwH0IDkx;xuTFwF`lsm~s1pn*8|HLw^ZWjtw8Ukmwk-'
            '=@S<GTx@a5vK&bw9(uJ(ZF6183l2{f>6VI>fGZ;Rr-bQI^kR*@{#hfC7gMd<8~y>O03Q@Vff@)eLYewbxOD@&i)M'
            'p&I99TY%dGM7y~6H)^hP+&58ux)`bG0H^w#+~|>Ei;$sceV-z$UEtmpdaA8Brw})&r;Lcm*LDWOn0H2(q_j9-'
            '9_}i&qNT;v3#Qt6o{MZOa`GTcRjn#Dg&PluI7twm?g0jLu<8hs0WLxaSI1!9&F63;Kv|#V<7;?^cEJT4!nt(Xyr!'
            '6OR|_zo@cZL=bjbCkm{W`Az%|u+p2wc#nCQtM2b2iK}2MzYdpiD?T`){_PRzQ^}I+rlV=!CqQwV6q&%VcOM_6BW9'
            'o$Y2f4dlJeViVF5!rSH^^|p@jTmKdeM;fE7%|`|E35fueC7U$WfxEi-!g!saaRe3;G08x2;rNrU-ipsmV}bO-IR>'
            '`vc`BA0@wszv>U-'
            'Ur+b%v2d3M+}N=}@?@XNGpJ<;!!aFVgeinlk()%Og3aOcAd#y#$pyA&B2i&6Xop_ydn69<Aek4R`dcP8NDR*;B+w'
            'k;|H^VtG4s-'
            'PE3(CtJ25n&VZsAD(fiI=1~{qd&vbj33pE@foPK*WOC)_vhnYTtsXn9EfZ=335w6STj4kYwTBTv*B>mX&s`zEw!O'
            '}0!x}T}=r?gAB5%u|%cL1{g?y>=0JQH|%N;Z$7OuT$*WNK;PriqCNBv-'
            '|ymQmY0*|H%84A0_W*R_y>#zOXUlE_nMUl8}S+p772<0+JGYny}(%Pd3f7!zhV+|{C7z1@{Lq!?v%UC1KhA@4<)h'
            '}>q95gTB=A+7Q}gqxsmGF-NOtHW&9@UmFUG=T>%;~|dlx}LNIs|Hsv)IIs1K>a&Js_HrLEq=C{PODG-bh)@nw|0@'
            '5W51F1DbqjBrAEV09375<8X99iUjD&US{$veHNG4dg#^e+<GEL6ye4UnG*@c}JxObC7O++Tm#eb)(Ax?c>@`88Mz'
            'GmMzVEd!$`$-~AR^_PZ-Q@bS`-D_tDm($4%n_Tw5bo<mm#aT<Ah`lc3M}QDp(if;zOMkhEB@Eu5x-'
            '8xxG_IYg0i2$3+6Yr=9w@1dCh2eChUf+13_ewWu46R*JK>_5h9txkmsgX*-`#$OATc4iw;VN5864cU~cdkenQI-'
            '6T?#jv;V!LF`I2uY)z#0P<5{`!xFYK^;|YnYBK9z_=MwU`8xj1Px6rUu3;5x1+jJI<*eP#CQVtLv1f!Umd(PghC#'
            '(^6a{9Ihgw_y~NF29eLai@_Q#?yM@zB+m@jI&9Ys@Z$FArsfs0T|MBOqVYZ1bw5x+@hZR4-'
            '$}<gYg^Iq2yNG?QZ!t;w>WzYY?TRx(>x}x81-r`k3$m3x<-l`GM`-'
            'boX~`p@7>{<*U=%GPg#m)4|C%NcK^PYmR6AK;i=oDuohn_1QQyVl3OFS96T@y6LQUNwfVxtw?hjTUylHTRth-EWA'
            'qDQM=k!ka7^{vGw5<T*ca<d^K2QXFkYpzKR52;mP{KeZ@%zWfVXEMW7O7Mi5m)$W=M;ZGfk-_7v*rgV-'
            '@a5+Ox!NmrI>c{S`cWt0=n(e1*-'
            '0ySIaI<;j(Jb#L;y=>+O?h5hP;?37o?VW$`reQaxbG_<P%q;5Fv^#P`NT)?2qw_2{GInqoEY^>xaQS&Tr7YxxnLy'
            '+z3FuCaEEij7KP?Tjbpt9r1{>Vb-AObHDaZ`|UW`h`BK&TKAXX0-'
            'iOX7o(&;oK<O<yG}|Z&ueOXs4B0hm&Kj!*r(BPE=6cfn}!w3rys^y2mV}YVxCAm$ML#C~rLuEy~6Iz;dm`cgz*5A'
            '%U0^HJt2up~YVZAG?gUn)1y6cWY_?lreq3ntCA@LKEm7ruJavfb!jN!9JNKUp+kbg?A<4+a*E}+b!LKwd4OvrUq}'
            '#^h+l(pPEK)C;CyR>bLSP>LdqnHE{-'
            'o$P2eZKgXjNaXLm78hI5}%1_0Z>M!AA!Mz48=~xe33`Log=f$n83yaVAXj=NIp7@(Wjyu0JTNO97mXR?v2z!vA%-'
            'Zi9&s^!8_j-'
            '{7GH`{X`%;MBYD?Ftn)5q3n1&Pw@CTugn5zi6q%0Ui!7ydeTt67HZx1M!%U*}%vE9OnIbfVgXOca#La>){wEy-'
            '@=1{jXs_XJ%SzCc_FPK?vmXX~O(jTaXM2}(jq?aux7NYBi=NkEO6m>|XkZvl8N^@i}E&16AZlI4tqIW|MMx!Z;m`'
            '<K*1Jn?cVK(e^N*!SlS}ICXqeC@Zl3a}qvMRr{kK*?2K9WWDc%+1afeBC-'
            'E&&d&X7wdxl~mswp`hP?k!D_?H3R96KsjOA(IHqSR;E?6?kp!Y3PfWQuf%t!VqF%~gk!O|>U$+wwq~i_iLb)%oV`'
            '{t)|1VA$uF<rxXrMl9r33<#mr9Le3xLg?fDX7=w`Qq$*#*)MHlohVXgk#T`L}Ee<-'
            '9XeDT~5a?`+DUcp91uPifCcu&e=f>qf3=UJE&$A2tLN%BElvT4yuztw*2Nn8w!&2Tf!hP>7)zYT)}CJpyPpEH5W&'
            'tM4eLj|b35u1>FeUR+$=rp(Z+ix^`AH_s*b<E07g0nVlMlX8#4=&atY#T^3;TyD1%jpKIbg!{e6xc2j914#=7(T('
            'i&6Bv_RpHU7ljSHRs4QanRtpY===5Q6Z|e0+NQA+66tjaaS%^YH|2GGUR6}yTEmm{Yq}<>Od5I;Iy7;DTQQoS+6b'
            '*!D$uK^!v+j7qU8+H8%|KwQnF(pSFU~hS6(@$u$Iq%m^=mQHd|J>G0Dg2G&Mfhe{Nd{9jo_unkn+21O%g6R@f@UJ'
            '_<tV-Bc9$O-'
            'xhpYGvfy(RREW))zUra;e*}r>>8kDI+9<rpxQs8R$4rLO1_dcfs~bgOTKz{oxxNh`lC&82lk(4NefNTkd(utZaZ<'
            'VX=ZeKtB1_qWfrb8Vaoba>LKdfE)|9N#URSk>}MT%1x^p=$Z8CU-'
            '4X20Sdg`7^$Pp9$^YQ8J(Sz?v8+L1q<^J)J}g{e8ogOP#*F@)i%T3u1_npiOgeK7|2Bj!x(3Aki|un+e#RiIoof2'
            'oo8V<nG@e?UwgglBGMWgnOU4(ZMvCn;>t}(7rq=81o@>vs^&csFNyVvM>@qjol)QpZ9NP0>3B|(9pM;M{RNi+q_O'
            'akBCO|UVssvHWVsk_9c`sZUd%VL20wG(I{_Fl36*85kje|Rly!%LDd1JDCH}ci5FGs4sshj})LXi1wBP2{!Fwnb='
            'zJ+{^Ns%mN5jANaR&Sg!e-'
            'I{2lKO%Ki(!NMMgr|j?EFgH<C{yU@b&M9d;dmNzJ~c87Wzu_6rYvYGs|S9(^RyxYllH5dH^d3<abCIzq`-'
            'v3chq|my>DgU}X+<MX?^~uY?y+UJIyG^IDAb_yjATQn}ye?~fE?wPCa@%1`3PkO!BqBlU2xFIpOsk<up>KAvCKkh'
            'QbW`Z`J~`Z=VmXhPBf7L*i>5?qt=og{>^Xv9Df1h}+$T(U3V?ug~7uc-0UWE)0;R%)n{0-'
            '+fdf5?kyD0o^W@C6+giakDlfj{o^I|6OySL4AT&tcFQplaLB>yKqF`1ShM!?*MI$kg6Ll`H`ime17*9?ci9kggSL'
            'Ojm1Z9mS$LXnM5jH8}&jkMo?LK|K|J^kXFsJ<-7JznWwBR;!8!(JGhO%TJF^-'
            'kzT4ua4e)cmAjR<na9b==2R8D!4u?SvhN!{`*hO7yb8-'
            '_AdUl|F5H;CXe8Mhd)ie$o};|;J=SD@!@@Wbb(Fa?|;p>uyKk#>1_VA+26nXO8oEdFULQn7hh!JxBn;YW$sMQ-'
            '{#-HhL=~oO{3(=aKHQmNgL_h`Fkusd?_2q55MOR8~z}Fug0r-5%|<t-'
            'xd<go`kbhU({Tx89V^{YWSu8(AZz91^)fz{=R}-'
            'EymZuk7eV2{$2Vz<BL~oof$CtYI0lzSEJ|ht!Lmy`GKAr3))AMkY+vgLMTD&1gNxx4h397f(u`X6GIP^g;rufCEv'
            'Zcu})sRG;;V=jo?i3X*%{B@;9S|CG9<M<xOgT7R11xsnle#9;0j<q|V`VGn-'
            '+Pz8pgyK<XHDk!=<gy;&12hF7b4v+O?&hDDGl?~jfYiI4mMl%?Qvm#Ay585b0_N%lB%4o|Wy`GNs>B?ZXQFooQRW'
            'uJfqomN!d6n_sDfMpSvNJPzoc8T7hTjf|);WEo}5UMDTQlM_*%7CgU{IXaTNIuCOjjBH2tpIQEXl|~+cW03jv>U6'
            'U>z5$lBlQZ@3L@Ri%{p`>TH%Cy))u(v_<|UTnMigE-aqHEnPh0FVMIFRo#kq6;NA7*Qo{l5o%;csa>wEVndNxu8Y'
            '~tj(DCBv<>B|Q&Lyp%9G)J&J`$%ae{uBu`1Rqd{N&Z)^P{tXt>q<71UZNDyE5az<mM}|?t!$AS<c7n<nZkI@v+z@'
            'nxJ)YY80A}qpS%J@YdGHPTr~U_F{ov^L?=P+702$6B2DYZ*nTQpI$Y?OBmjK(;#&g5G%7Tq3#|M<G$dV0x4J5kTK'
            'KUYDJ$N`8pE_;TXso{>8L9a8{_;qiSwhyfqM+_>p6G#QEdjM#DQB<o%RYDTw$SQc$f`$&Eq4e}*d-'
            'w)cVSOTpU{yD?9+AP*^2i^I~CISKu_J~_~TaphE3o>XJZEJ*L_wTA{ku%@ZvEt}04DfBOY`Em3lna>BwtI<>O-'
            '@p9Ds2mI(CnE<gh$HtstyHhplplF0xKp+6qnz`8@a#hThqVqW>P$;EV`rJs0En$+eqrf!A*BZ?;`;#cjpJhkS308'
            'aBlmmiC%j{5TSld*PkCPeL|&r;Fi4(cR&&t~RaRcCS@;}*(4lvK<;*H%jYYm?+re=k-'
            'b0fM3Bx2C`d#`5$91_H2S{dKESEqttKvqd011%{`HOvf4v)s0Z$IG_9T0>s#kUi%=$FO7y`~AH+v>V#(0YVFq!32'
            'kq-'
            '~)Na<0K}A5?xvMgp2%>;dCIr=<}iWB7LH%_I1SC0xCUrX*x_x$jsc%|^Jj#${3AlT3(E&`4~TU1B>)d((c*VdZqJ'
            's+FAt-Pko~G)VfG<YRzS%LpA1Pzyhzv;3*MNEjW)?Q>3q?1Cj|{QJp8w*8bE_C=b6jGndQl;kON+T!O>x>5?O*1H'
            '(q+vs|b9xhCEz~c7Ql8<du%{Mc$qPu6M=}WHNer{2VFDA)yb2+QV$(e%qT6BK_Okay)6nR|>8iFNB#Rcyv#r~OLv'
            '=atBG|~a+sle@t90rN6p`d2_lR=E?sgm3kx!QpVJhVGz6&GrnZQ<w`HNU#r%+bvW^X+GXVpE*e;bQVq=)UW6G5KB'
            'yqUj*(;%+z1JX?7$&9eW6nnU(ks==6!_&~Ka8l3%6ZFRSFoVKmX`a7dH^b8q!YJ@)O+6oQ}ZNCbXrp#Q{pb%a_Q?'
            '8{i+JJ1GDQ+t7LL&%NkB4!ftR8ro3)R_VYwAx88c<o1p#d$0nMbn0=Z=2m4o5look$vKg#ZgExNKODcuWY>b_kN>'
            ')CdVNiB>bjKgRqJ6d%-'
            'W*vS;Jiy6W)L9~w@vj)U$63JsjKUO4S!|+TMP6IBJi*sP2!Ps7@+rZFe!^gunTMhWW$ZeTl8*!`c^scN?a1XaM?%'
            '9_ae)LpB(}HTW)pU8V^;8((wRYx$iEXAf<}PcYVeT}rjSV@p3uk-LTz}+<RcROLEDYEzkQ<q(RPSvvbQ)*dt>WB&'
            'JgXZcn%{vlaET=N%Pe2lvjemgKiN0J4=x+yhpz^z;0hiKJPLw~=QLy`?yIq^q^G5#kyH@0XfmKlil5FPE0dVZdpt'
            'lV@b$uo4TnG7&~WO?b>*bfTyk9yX%jx8ykMnETQ(e4XyqJTT=O#{gxchnw=yS%R#cSWXub_~lV$oBD-UR?DEFF=t'
            '7vAflKfsroa4F?3gOOE&*3xCax>amh)Bp|PBrU*&Cd*<6$9JY=(!IX+SsHg!hF=GKJT*{;{BFMT?|?tYgoxjP2}_'
            '<PbzrIGOnAtDAJY>clFtW#?s6QK|Y4#708X&Z0HLVEnvp!Qkq3UGb~~ZOy8fQGQ1Q+sA@%%<n0fyVPBigoT?ScAT'
            'm}e3`aBs6qPGY{3<rxmKnW?!n-T=?SvmYD%sJpjmVN_3^{n85BPu6bF~Hy9_$9-'
            'q_hWQv!gLH^Ff3PEcf3+Sn(&C_WJ3|qt_rIIshL-QR<1<wPumRACnT&bKrxsC6!V9G@qqL9+rOkx(2miGY><%saG'
            'FT3b*|0u!j6~W>gl(dju<tkg6u==!4j9B}y2{kLShe10RIgGX-jb&I7x*n3~aDJHTl^>iq_oZ=9Z)r_d1~9kaZJ<'
            '9IhRE>b4DZZJH_XA+1{GbG5J*Kma|1JW;s^~brOO}KOUy$ek%!XIq^b0l|1uowjVABA&v`#Kfsg7g7Ziw44slRLG'
            ';_vS$*%Yn@65o2vwyj$WfIAMc+bW5zP$0k;9VfNJRztT6gAKZfY#yBY~514@2U9bgs;(`2u;=P!#=;cRh3lFj!oE'
            '@BlAv5g(y&M^1d}@;=n9;)2apuPhh>cUpy#-Sg!imR@8c^Q^4Nt2p$m*>`4i0R=Xh@1{xlR6BUs^hy5$6>+-'
            '_|)$Q9i_Q-KbdlIy~f7Z}CqR8e{~aXa-bG{2bmSk63zf{GN2C1e)8Sj1<y_s^f`iUA^daOo+pD=Wm7+vTo1ez&}_'
            '_C?F=_)*SSmBw6#SX*|L70IysBUJprE5qM0jCQx_i&4NUOi8P>yJ@FbDWOC3qSwy)I7y1gUR78_1z>b$}@P};R76'
            'egkknj|mPw}&J$-wPt5zfG-Bg~0n5mwuSMOSu!aATj6Gy(O!;j`Y3nUxF_Mk~oqQ$1vIXN~9h=7lymiDp&GcD&oP'
            'm=AYbo59#a+)yejfd`Y@Fk%gRcmH{@r5utL+E!(;9ciKaXpk7O!vZlygE8uHIXX&e!8#)pdKp@%b1DMw%*}Nl*hi'
            '$TF*7S)j1EXOa-Sqe^3=jW&Oe341C7scBf#&0#<bVS$NYi+DJFg}t0@`~k<m2Heg{kzAK*Dmh>9(C<4&ZxD~Yc$J'
            '!%G(!^kYGYAvw|1folJ?cI)e1N5SarD8S?J(#p*_=$5720te@@a5c_u3tb75qT0$P!Ig}Zjy3i#P@dZ3#A(L0tt0'
            'Iz*+K5@?;b!jJ}<t_*{ke%4IG@8p&isFFQ)Z1C~ah64sybI^iMy8l*P5$L}0`JxZS358HA*_)ne{!OGRq)S3Q&%h'
            'vs+_zEeN8&h1YS0D|`AY77qAjU`;tC+kY3YwvP-'
            ';|WpK(^U~QzBUGb@8zh1c_n2`eaD+m(P_MUfDpbdevNuVK<9P2*%1gle~fY+R4?XY#M>CrXq<Kh!kTds$%9%kZFS'
            'lN3%5i&6ID{CRtarS>FAu8)iv86Tveoh3-'
            '+JWi<TPz+etaT2eE+w_J$2rJhp2d@IisE$6*Eq4#<=7Z;}B=pG*vnt$#C&(4h_YV?hq&(D46Kzjq4pm;<&H?hNZX'
            'D$s66PTP_awf8e3h5g`n()Rc3{LwbHT_cIZw#j&SMcJ0TVfXfzy|2gJ-Xi6MjM#b#k}5#eeks*&O+bVF!sHL^b80'
            'j!+YH}$p<MXpnCLNiW)}gN>9)*FU570$i!k(%DwYutlx{VQ7)mO5<N_Rhxr@GF7mgY7eCsj9=fWb^SA5kFf>G3I2'
            ')P*>o7&Gu=W`I>URpLh}PKgcIFg<S|q^<o#q&~Ga#BOCjm0PWS(&b9B#gCrqwhf<C7eAPe1;xuIKq0Uh}O<Xat8S'
            'XR2Z&jpby2B@{A@)+Ifd*Cs<!rM25INy$jmJ$wUv2{;v(o$2z4k)TVSCh3kkKO$rZz9j8d9_zxJr8(TSyOA5qQF('
            'sNm(`t~nC|-g+Kfdq?ei(q-OF+gYfgik25DTtjL$)%+~svmUCd-4iin-KC2P9T;3YS3$p)8=c6ePXsZ}TZ0z6IXl'
            '48@S3NcuP)kN;e;kLd;%g?NYM`-T0+Y<_~1>%X>PEUp1W7^aC;mjxV(9EQk^ZJN7?2_<-'
            'c#XkhD#`HkW;34`lJTq0qrlxT5W>qE0=<!wV%}eTEa1EVP=_)h$yLD|n#YyQ&un>F)cnQk61)jiCs<IlOMvV5T#3'
            'Z)8M+Cwuo-`v8mvOCYn0rnf8Rg8^U!4#CZ1xQY@UkAdIc1P5T}R5p{0!+7D|2KUrrCbTC*=0H`OoqsdXa-'
            'se~&de?BTvuYJLnxHqN8tFq3xTp4&Rgl;#R!;dmrziHqZCZ?>`cMjxtL5o8xjaMy`%#2)S^ce$*rHMehJiyoCm-Y'
            'pw4rVoq+Lgk4W}7&q{b2NT|H3j!5FIKTz*8sf5CWGH_B0(1he`j=>az!h=8}26Dznt90&Em*2SAyAmfC*K^du0yK'
            '{Y5nu^l!=grsdH<B^Tx4yRo+<KVpg!@ld}A;!==U66`E98k|`xYI&nJSei75CiJ8jx%%S$1fUb;4tjR%1+=eKvPH'
            'iM38D*r*C@X!n00am`*!#V*ZCeyaDL_=&Os&V#4W93+{lRRfv@PK57YXqOaF;4!-'
            'fz53oxU)9A<>_7wY`h;RDWe6g8dmMi39QvB8<Xbwleg}L9rj?~J3;hQ^S5}3Xe*8>lMh)Jr4hCk?Zr-'
            '6rhrzQH5A=2e$Mdk@*CAcmN_)TzU&<#*MfTwM+WaBkdP4mXD_(#vP8>h*CTU<8FXJViEA8v}0Y5Mi$H+Qg8!?GC{'
            'OBsu3$0B9-Uq8P5=D@t$tUj&JAK5P(!+(|;9+mcBCJM^wL#_f$e`lD&)w?%D2PT97-'
            'Nw#%2Px(@ji8Jfz1;fklgqElr~9eXKq8f!3yGqf;mEk7)LKly9Sh?YTL!!Q?@z{0#+?T{e)GfOtK%1PxK_~r{f}R'
            'LwcmXmGPT#3Qu0>oThm#R@>NXY0K?#`-@>viXXE(jWKS&Em^`OOLgw-'
            'N+{;ic`P@*@_Sen&c2<5PzF*dp+vM&}(8OXbgp_$T6EaUzESkLrGK4*&A0S!aDEXJ+SIhOY1Tiv7e*1L)>652lK1'
            '=SwPI~=BL7~P^u&oeEuByc-*%$xc@0XvFeQv&l*7C<E>W8l%^TfWseqtXOlNZ225x@7oUVbCal?-'
            'VZ!Rbk?PJ!$vXw#)*%7;~ez!(oY2@J)zm7$@so+bgAHwco2DGOf19}SS9zR&CVWwoF@b7uFk{%%0{`tcG_ks#&{Q'
            'bOw9x?YX|<IhsSk^e5cN&1_4Cc&$(E;QcjJM%Ey%WX9W5$kYy9QDcW0~^ECo57BY@dQb#5J0-?ZdTR0)T|B?w-'
            '5!iCx&jh0ZjqdzY8z^Q(SHK%Mr>ORV34D4S4{Bs=luFV5xYIQC>Z1El^4IPHxYtN%@ClMJ9$o81t1WS$c25)5CQF'
            'CIou@F0)N3V+5O@!O-'
            'yYrUL&JzP_TA88W9aya?xc4BxGvLtXW1jtOYqokEGlLGtcQ@DTX#I@II4O(i?%JNDgkpiOO}e1|y?jlW@=Ulq5tY'
            '1ze(FqZWRp01maPA1bIfga6oP*vkaJ;n!J%HD}Ng0Ll|c~sqy5BY^Rs3q3*fvp7O7L#TVQ!nj}n~!@K0xk0s>DHK'
            'i9?}V!M076{q&tiL@4b$vC1&l0keMf6?YqB9RP^8Z{~F4F98ZR?$~6?zv<zD|l(#GJx=?J6f%c*CefX+aOpq6}8^'
            '6+brjQSnM>qkCOj)$9lbHl1w8KfM$ZSdbh&w_5v;&O!_u*wJSXrM|&_0=|JsVEk=1fRvC3Y&eGz-'
            '4uU8qd~5%o{v@4lSpP=6bq&Fgx7eNugz7t8aNxR*f+bgKtbRO?l#oh(Xvw>_J9y8S%Yx-'
            'Z7w8#}rvZ(svMNqe`MDzy}A?;*rHDoL9JmTiu8Co)NNxTz)>yiG4}c(VAh??fb$l2le#*K4;ueRVs~-'
            'R8Dk>9d1R#P)|zpV}6TC0Tg3_S^r;i4dvbP6^M@@BQQtUi_FiQwkpja`uv^!+p_*)??$4b)N&9k2w*})Cg$wPfEw'
            'MYGrKENBue#26q}nN<=6?;RZIfgxg>+0TO!nckhyq4HdrcTW5~Ec(79)5RGQoiyx7Ot!=fN3;A!e5|g2BF5O6Az`'
            'e65fq$yzo4E(UJSj-vUj^owW1baw!Wk;s2I<2h@E>E2c5Dz_!gdttnTB!jg*8Qo2{6AcKDu%I@~1U0*BLNLIxqu1'
            'IN{bfMBf~5V2vK!;>oJGc}_dqgx)7Oa)**NP$&wYDU~U$^A8qj4I&l51LzG9b=!j}i73Irgk%Fqw=W&c=O^?Bd<='
            '{X_mQ*Bk0eVCbX1gJ<^5MIHOfLm@sk?do-wUGIjudLL$|G&dSAjL22kmF-y}IH*aK$|tTl!36fBlT@-'
            '08GQCxFKup;H%&;=T58_ilG%_4HREd`BKs>fl~yxGiV!TK<msEO(i9I&KMc`KQ1Wo=#f<b{h382D#cph64}@ukcu'
            '2%fJ&LWK0o#<vbN;DpR_g;np`&Z0H^r%1KIM@ipm$1)3)?lKlBB^kjrpT-Wd1?INnaPmfQ##0wX+kk-yZf__d4?1'
            '93@(kdUL~ew4J|SIVwhY1gM2G>T6!w)_Fl!$aHrK*ed-'
            'L;XH9r$ZWcL;=g#dwOXB<@Ya#mc?U(ZVzIojzzpc_mHd!Q^)uO>gPie<QT-'
            'c||BHX}w$BEPA%`cLc%;_tZcgp+1g4I7%%!FKsRyoFy)|M2@i{7agJ@0s|1v>jRI&2dpv-'
            '3(oBgB`BeEl>iRg9>5`U1Xu>f+rNfY;J1Avbh(Cubieq6%DPRTF4H+F7$HY%Z&mjS!S7>%+e87*&6eQ*1|PGUH#n'
            'F%WsNCDYjyFz;NK{=`uqH89QYPjcURHX7VXDo9P1?zQu|nUJ>cqGrSvSW5=x_TeEwD9EqlPK!Jnz*pp`}XMN1spc'
            'B?KWv&tt^~JwF8g@~9UT75>!R3io*l`F2dqF7Unc_##B2|M!hK$(<4SRr*Wd0yM20EZPve_*Jy<-'
            'Fu#F5{6hD3No$Z-'
            '+s^%|PRhGujYO=MV1CTeZ{bZ<}gNCz^_`hhgk9=<tz_2;wWv;58B>!Uaj9Zj~k2VqKk>w1r)nGC9@Iu!>gO1k-'
            'awK1z2yCeVG+qbVFlg-ipJU@DKex@5<m$T(TI<3gWWrue`_&)~P7uv!qUnQhgkq)`F@FwcRf+99}WwiPD5mrdMuS'
            '{ax+&Hi+U^(gW)uLW0Q}W|kv4Kp@Mn)~^<z}ZR!?8Wus<9$O0G|I0udkIOyw5i2k+{hCEIU?jEL_oCSD-bdWPZbZ'
            '1w>pF;>UJvvwRSgYL%@i&~H_u+ZXN1xGtim<!nQypT3ouL&Bt=kwMv^%Kq;`fttoHX7JGMmR|{~bPLbKh8C;wH9b'
            '!UBtseciACnPBZ8~nuCHsTGgXc^YmUllZkwV0pzGww9%S_wXZHgY)lqX62V_#>oZU|E){xe94F*TX4EPuEA1zG{*'
            'v1|V<<G!E`kB}N&@8QVr}jB8PPzD4t!lgi6IL!K#+b&>xbL#by<+b~2|2%?hf-'
            'HqRiiZ;nS)S&$<uLJoB(Tc112`JqA}C#L6xVL@Md-aiB`S`2<+Z7c!9$OLYi7Rety6Af>_9^oMZO>N^@WB{AqK^Y'
            ';(bofEH>*1%8`=ujcSlELlwAcwNqauxb>Ulwf?NYFWkys3qln{L{DfC(p(63Ow@0->>N!6-'
            '`YS&#Jx>q|$gGPd3f<w^W?kaQ?s<qt%7K!n%xKesJccJQQa52fhorDVJuJJp3+SMscZ9K{gGg2$P<|V@b+=##3g-'
            '2?%bRLsF<b$9l|xlBHC9Vu^*lR9nB;FIIC_2TIIV=a90Sz`4IATX?hy5+Idb<9x{~d3YLVk6~u5QJJ>f5&%I`oyv'
            '(s>2fT&&Jcetytkb)nFT5|dEkYO{R&f!E7X`Db<yZP2XNB{YG1F~!sP$_um4Xw@`k1(&jKs90Sp{Zp6u@rl0QgqU'
            'U+1zwk<?L&>!qCL$M<KcewlEdcCSHq0TS%1j<&QhCd$WFG_f_^>*<bl7>mAlm%&qR1by|eFlgOorkjm_nWbNvPWk'
            '&P#yaWWgg71eghIbQW}K<>UUs9n1srlC^#V(5%<-'
            'c)RMJ^_<RyyjGW2JL;_0r3D}a@LMW(pC8V*H^!)_@UJI>m2AUm&EY>&Al9xiN!-'
            '{<L^b(%4Swfza2{;VDoD4%?aZ+ZuCbe$7kW?cV5=Zifz`Ze3Bw?jimXQP%iW_VLvv|9zu0WGB&@1mQA=CvIuNVZr'
            'Sw+>Ks-`EHTdo<l<wGzD0STB*7=7E}sYwgub)w9^+1DXM<*6Fiv&|eNyr)8DB^}n{wV9t+h(fJZM;Fv1uGV8S8-'
            'GCOON_@kqj}%_ertY-VBSA{<3a5p`7*NBECLK&enRN~8&v$6{Ryq|cp?K{i}z$>fDl_L_lSRg;S4n}xV!kbrs4FW'
            'g&6D^(P<Q$`z^m?4w!mexnk&b;xDK5O|$#RU_IVxR5UlAiK}o{s&Ac#JrZjCIaQ8p`u-'
            'rs&w`Dcja%1JW458A1$>zF@qTs=3qJp=Zw6WiHv$OUN7~_BdscG8ZHWO#iIthNL#{nPr@At|m9tqByt}0`7qoxH4'
            'B4u^AGsIl@<rdq1g5K{=U_UfHcNFzM=O;hAIval!LZjd;wp_aIU5&?1&ChOTbSW6WOuy?X22&lGoUIK*4`s-'
            'Bh{NLsz>L_z<r(NHPi#0-a-'
            'O9ua+$>Z30HHNS<=0m}I^eqj?gPo@3kQyjK3#=ph+zR!}DXxmfLU(!q!0da(f401J}xB<HN7Z@HH=Y-'
            'g5WCtlS^uZHRpni(3&>W!c(R7EhRNhv1%^n`y735r;tFWl{o_$kx{EEBm(dJ*nx2}mIzLdc19mBLV{7m{~g%x00k'
            '&*Asva5f9e#AxQ;(o-DXlNT?e>o#uOmX#YfSOAb;BQgxikmdX-p|liR%nYk0E+)w-'
            'Nn7c5q8W~b0Q<qCX4$HpbRwM>-l2^WPy~Y2w3Un^0H6WL?H!0I0zoy~MpE1Q=UD7<Ihl5*Ee~QZ$oy<98DO@_5-'
            '~#TIxd&XHNeOvw&gT42sex}Y|)i&j61?tHcquJX4SN~E+YydK7=k4M?-'
            '7XNnAQ?ozP3ye$Us*%uw#0kyfPMY{RmJ4o8A~r`gz>**YQOd*od~S!O`hqVc`co9~h(r0?O$4iJfBX;#Fb?QK(u5'
            'O(XFUKrb?%Kr)qnP85b-!&|~kfp>cgZnI`bs|Q|M}iTi4OLWN?RNVzq9>(wAxBh<o3N{&g-'
            '7c5f*k=+4oDWb4X$IeXzJNVQo{L-<sLo)SLh+dyZKPTbGFunfjGzaM-'
            '@sv8@eS1;a0{~5NQ!QyOE~)EJYf)j62fI+Nic^dE^;s93uk1xyj=k_jkB_3&?qfOh`SmUaZ;KdR0Q1jVCeLl4V8N'
            'CnW#!n{aJU%c5;|HMN+1LqkJdfE6G!^jN(g7uK=L{aJOj5Nc^)9+oD+YJ7h`>jaH8-'
            'H5e1UlAnRZZ5FGX5+rsaR8i}o(Cn{f&`4(oMGd;WuSg90E7LRVh<D~$52KJm$BMPDMmpPl;2&39QXZz2R&${8*{|'
            '))S^KUE|_nN@rNra->AZT#{W|OVf;ro%m-hB#-b&<fSpdqlgU#b?Cx-'
            ';e;j|A#%*V&zG<kN9rlEpP{AgZ&_QgdOO>r>OSyPrS*o?ARXR=%w&%~baAvqjea0v~7lBAyG#w4LUBr&7N6b$BJD'
            'NqAGpg;Do#4TyE|thdkH<L#1UMQkR_|fA6YLp(BN4rnsjCSvmf&#*!+$7+McU0!6AeJr$=waN0zLe>1es_G;XZO;'
            'Aqt_$md3%E0zAt;!*KKViHDAHiT@Xh2c<XXo{><HhDlT%(A*(4*9h`&0Jx5*kER9N9RXoJ7UzlH@}m2O4-'
            '@S?TlXeKgi-O3jonI-'
            'Q%)P=*F|tswB3I$!U|tsUGIl2Cmz_94w#~RJFTfn>{u=<rIX=IzteqPUo&g3ARgJgihlqB%)9-'
            '~PTyF8nypuz(Jc#=qR{t%eIGhtNH{Zqp^z4lyyOFBv9`^eU#wfjKLO?P^TH9-T-'
            'PPZCj=^xP1J)8dLVs%zki|RnxIuaHifnqI5Kq!C89MDa^cr%!aODeFL8-+rbC{a`vbd5{e9ZedDE_mg!zj&%-'
            '8h|_%=8#vq@%lTr%C<g1yr8n){y?q3Gu41OVOsBTVxgh)jv~m34RSn1t>hTVp?y^zay?=OG;#e+UA6ltcp5w<ffU'
            'dQ2QaY7lL0`ighqg43|T*7lT0M?reVktVqYvlQiWDi`pGWU=rJ9NQjK1`XffOJ#qj#hQ}+Ek^H1M?q}K*CyIr30<'
            'p{zS?MWHmO3oY<>(OnQKd><j5ww>8!rW!LlhRmRN$53)NCQb=gR74^_w(3B+P~`|_XPMACCR+_^(A7?zE+o>hfv>'
            'oPm%u>Avy@!@iCB$2IarAUR(0EcT1{D8}W%FFGt!7!nBN_A=NU8QoTI$@kxs#NZ*N*9Z#L46J&mvlWVV`kq{!IH2'
            'C<RP(kd>t72zZtk9Ul#Nky|M8Os|hMIZDtH6LZ6Hy``Y?!YKp!&KOM=Pydg$xQl_Dp(pprIX-cy>xU-1z{qL-'
            '~{_f&8tNYHHiCIF`qO@*xS@=@my)mo(C`X7~eWaF3e53FPw``P(CU>!V$6fBztUG(~UI=XoB6Ur3juSp)p>u`6L6'
            'XZ)Bwov}^=x7`f<KK0-'
            'OP8I>05%VJ#Be4wT0sDBy00U7Qv!xD}~m3$rE>0aOZv28F@G44)c5D&(HELv_>&II|0wb_Xn|=XRYHH%Gh??Y#At'
            'OdFx~?e~|HsuDG}fs)Oao2$dgJ3rar-'
            '@93jZI?=eLm`5z#)}yN>$?zja>O^Q8Qi4T8@yU?Trp>H0w#%@~lV##=VZ`oMyWrPDzhnKd9tOr90e4A1Z$1J(H+R'
            '6wG7BCme0bugntd>egK}fM&VVg0(MLCh(vDZKxi>e(3PSF7-WPp!&z!*S*2B@st{5)-'
            '*%`r6!7*qW@XdY3TK0Ce{dIMUbPx=cK<LPUOrh-)4{7~O)A-J5>#{uGynWe7vAykb2@-'
            'l2o#3+*Hwjb*&4LnRJ)B6XDk#GAZdT>d-'
            '+p_qHVdOUJwu8BQ_)CUpwfK~4=V?WzTX9B=KOH_F&S2t6vP2v@Tp?2+kr+ya}rJ9m{6w4z;Wc~!Co#cxHiDVX5}y'
            ')QV!F=@bJ)`3Ly8t7(xVEI@q46#lp;}3txadoMzc<3xZucn-cGM>6XB`!a#;tq3M%Z7ydUwHHGP?0TZ?!S^>cACn'
            '$aDmu)2|+1Vwkc&OVy6>%91Y8UeIBU}E9z&<O183-'
            'myiV|A5HSt&3hmzWEqq)Dc>fsePv9ypt>5~vic+GxQwZj#Cw+X(jl|hW!8kX%h1n3bY@&9RIKe2-'
            'pB&cYBS$hY`ERbYO6|IMCcwn*Ccy$^WbhuTraJmlXAH=`m*%;U_5744anS}HD!$BaR>K`URbI7Xc-'
            'o#8qYAI>_fe#5R58V#Tfdh|yWZg$Ub@+(I&p>&;dq=ldX?o-'
            '<<v^xtyWl0EeTn7Zc<V8zrD(MuXp~O{nQT^IJ4{nYgr*np_|(994c`yHM5UVb69$ZbZ3}>nJVZ*L7mIN@3;YtuL<'
            'UFCV<Oq0!&RCE*XusePQ81Uf_&3$-CJH+8-K>3ysj3IHuJ@1MeJ_h_x<x8a+cqIps-'
            '?Q$1wSb8ima7Y8rw=(O#63e&nUsr8sII!ogjfLsTCJs}O0xoU9j*0jlx1lBuFN*5thWRerE_to&&I&P1c_Iri~&p'
            '8?HwNnU5H2J@x&&0#)+X9>(+cA0xD?J9(v%P`Vb>HB{_-'
            '21m;?{E8ie;np}7mvWhpQn;mY<1ONBB$g}Mc0&yg0Nj8a&NHk<X%vZlYU#(<=oxN(f*f{dvl@DI<h`S?hQF+xLjO'
            'y*|^|M_<0OU4=|@Z$gGlf0Q2y0E2SB6=|le8GC$<Y*!{gdWK@X+M(UR#Jmv>Z6w5JblU>)ig&hQx;GNmFUngPCH2'
            '7s3HLz=3$*Z1BP;KA>RZTI@<)=l|D;OsMvai|b$ac6Mf)dK311ELD78mc7pWA4Ao_7lb&P<GZSa>OtJB!M}f~u+O'
            'KJ6qNYT>Q5oVG90#i@$Q4b!u&Xe0EmAK3985ts2nd?+(sa;s_cSqtfP;a>b>97v~Af3S@K=(szo%XDDwI^|zWyRr'
            '^9F*6sD=qNe)(m`0<=#=AD!oo*LpZPV7X<Ybh4{L0oE*@>R5;7CbYeAK{xJA~tmgd`U;o7b`<myBE!NP<`-'
            '~n9y+4(!`zze90ppW>S0oDn43y4jd<fdF{=Kc&Fnm8L*kBxaZ!L-'
            '15ikvERO9l}ckJ1zTU^51xbh??%ZuR8@6DMOJWt9_32iz+TraH0B&tV7fG&Y)O0u&WJ;WpK6G2(#r6SEr2oRj6a*'
            'a!sC!%tPrWWH%)dPj=Ujga{1Bh*!^<nz`&6RATOE{)7Z6V<~V)4;MUD?{Y4J@hDa_0?`E?-'
            'eu6#*H|(0efp|>!zi0NLwVVS>@v(ZL!F2HShfsnaUvbM9kI9vLevsbD7b*>*;@}No`!um$MR)5_UL0=TnF(ySb~`'
            'y|XSnmi;D+iOXVv5w+hlX0htmWRXKU1s4h6K@uw>O|$qAio%c{eI7IPb`x~F1E;HKvt_%G{2)ApnKC7ZCveXopRt'
            '%sRm{vZ-H7m3UZ}_1LSvnM2@%hmC9~oL`3eY7x1Q9X)$wopBSVfKj`;o+{6C)az{kXc+zF27ZF@Zt?-'
            '!5$+_@ScN8OD$ztpAi0INY~e%;Qq!+e{mu$y~hn~Ni^@Q3*Fe;W5hgb95|0n%bS2K4R=|7E){LRsj82H;%?UJ<=9'
            '1<JI-v*<o-_8Gh<Q3>Z4x=fsuw)jHopTTPaY*I)mD+m)e6J!2rzK~t~8U{tUL2B-'
            'Ewg)>RJXQWd{s;NKV4`9NBF~(R$mm${6MpW3{5N)t^gR&~*4;NF#J;;ooskhoy|@8ME!xV`5w<8aO}SbJ9(?wq);'
            'sgP4fTsL9JLFhD97jVTkg*ewzZ%mN4ad6M$uIh_Ooogm_MI)VK*<sgS`!1y$<ac>+Tluj@I#ZOSxhyVCzmh0NBwU'
            '-fiJK3Q`Yn!+7o(weYYTWqrM>H&@r4P$E4ln8^DZ4hu-IP#MVnb8(|@^R9HGjqcu-_KPTPLVh4-'
            'eXJ^xh4~U}Dw*A$sl@B;s7OP2RMnb<vRi+M+BDlyxf>eeDD3Rn+10z_czEbaX=f_r>!CZNwV`zQ@PFGI@90v=Iw%'
            'sK#Xl0XZFF>s{O9(GnBqxTGzlAc|I3&1U%r&j;7cJ){X^X-'
            '=r4)v(0{p6{`0y~9_$AB|1ImXtEX<|Uy(DR5%O#Cubmx0e<zmZ*+>;aJ9@V6^hQ10Yqbk`b|=kWMwTJtf0P^_dW*'
            'J`+YY40WY+F7YjaxtBFABOZ=tluQ6W;2;CJ;4S|s=P^~0gj`JdVir_<ATPPf>Qj*pFNP~|n3uhJ#;T5~z5bV#bOW'
            'cSC?MqRvz<vEgb)+yFx(xO~&fd^+i`Zbaqb$Nm8WIxJwiS$fQB{Jm(^6N)l=3b~8*&>?yK_|qq6aTQ;I2vF6kfc8'
            'k7H?#7ogWWR-yFaBZe$p&m@+gn{N?Kx|ISH3br?62J<TQj8>^PKy~1ugK+X~Y-'
            'mn<M3S}%J=lqEjsZ@2gDTz9IUm>rms>s^(3$q-oKh-pq6hdw^s)hn6tXGKwBh-s2G@(-'
            'T=yOXJ<&8Qby8Nk{0@Y6iV?VezHE~{*V$(rBHj0xb`SF{xlcVS7Z%^~nqwkK-'
            '&QJfGAD*9|9)J7&`OzSGe~}rrd+GTO4TEoVoFVldc+5gJ^-'
            'LQbsjG#u7;}0$hA=A8Xp$C+BxY4#hf&A^>euy6E{oE7n>pYzwUM3uA8@IHxS=<)m{nM@LYWkof)2%mA$g-'
            '|$4}}@U=Mm@SLKyxhEf=A=mYmLvw%q(AgzLaYaRet!sA0j_ZEtJT#@*T+$gdgKCm3>;SuaFC0d)6iF=VN3k%BSAx'
            'EJ+u|rybg&NIQcApM|l^CK|^b>LPSM{w?RK`MEX0`=N>|0+}MJ1Sy{S9B{2v$!XXGO=L+hCD&qo%V_BbE~~I=iB_'
            'O#GZv$#wO~sJQ;~I_Hwrq8*o{u2(r0CeMF1aKtkWS4`JXxK*5`>ZWF0ZpQ3y`F^c$7F3y(i>2~?i(D2yt7_6%KK='
            '5Ra(JszhEz<R$~~hv&@;<tgLe-;628k5`f8Qa2BeLzYgmN*)K{{N!sAf>rVbyh7CI{fhK_kV<6n&$-'
            'Q;EjsY(l5vcew-'
            'h}40AcPq_|9t2nPf?kVaDQIvVkm~fhxbi5Kcdi%H>I&3s6)1!11<z@?*vv1>)!XTbgm=uYOP&OzUv@$KCX&H3Ac5'
            '&iLKT@8cxr&Ris?=^V=uv$s}xCfXpr1oL+UFcERvy`<j$Sky<3`A-'
            '0VnUKyFkKiLdch$r(x)_U&K@VY05ay{>8cR`Bca<%ajNB0jtBvJmh_#^mA)#qYF<_e3XJLIcGxHRJ&6c4ww~&|Z_'
            '?64M90kl1hMX$Y2J2$f&()1%se)OmA+`9a{0a4!8YyOCFa)(gomEizD7<tVNPWj-'
            '#q>N+iY&LEDRb^%SUBr2%+h8cAxZK;Ut@{s?o7WA!nbU;f8StS&cvK-'
            '^&oKWg7KL66wjhZU(QWdvm1;ys!B;+~Rv(h|=J2cNZ-3nf)S?~V>myXmK'
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
