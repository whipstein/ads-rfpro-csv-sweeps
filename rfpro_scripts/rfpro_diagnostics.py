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
        '61959c94067edee9641befc9142a25bff9d54cd7615ae49568784bd9735d4fd1',
        (
            'c-rl~>2@3El_>fjPf;n~b&Rq=h>~NU4rMx*ktkcMHBcgLpR~-'
            'bfIxw)7FY$N08tE^Yn_L<&u|~?Jjva|HxE?>O3H9o(!CO~@QwT1-~RTz(=>fnt&7!Ux-'
            'Q=ri|b^$D&CjHRdQa`m&JN@olL4((oEhLv*bn5T--mZSL-'
            'Heu8Lxrtcqr{fWOKrdGqvWRgVXQH=8P1UzE^dx+<4z_^Byp1$-)!dRd5eFiHJi#dJMRo~@JO!xE-ws7X^S;Bzq>O'
            'sdJ^x+$A4o1~iH%96kQWjR?*U`fU5xcF^TRMVpQ%U?#xWVu|FMU&K3ku2-'
            '7S|=0u|72ZW!mKrpI^ey@Nk_D!RWXOvUqDA%5zM1DjN2b4PwQ3E)C=7Aw6135x~wbM>3T4oRLNw~)XAcr%xEmw0R'
            'Tk}<N=GpB*uMNCrx>|Sxjia!DLk=(^WBnO^*`T)&~D~24J8Mu!b6Tu(~RnBDt(*<-'
            '9Cr0Ob<|=c+s}0ZejVI|@F@yk6l9O@gDt?CW|3E4sQUDuObc$r3u$tHE?pH$^i}a6EBfFn4(d_^?J~nAHHFs$SEc'
            'sINS^L7Jw6!F*L;CV4*JtT(G7&y(_!ATg<+kJ#Wqep{Wx0-HkqeX+h=$bXlx=yhE$8u{UJvc8c2uGQC-'
            '>fCJ3U?G43>bK@v{S%L#S2mlhCsTj}>`^XFec~2Nm<aYOe?7u^>4)|8vaHVK_k-'
            '$s1h@)dIa?H?<OLud{5nb`CJqLJFOow*62^Ukv_uEI5yuSMX?=N#2s0%B!Q>4d(fQ`GsMgJR@Z|96!B5Xm@`INL&'
            ';NY<>^OgU@ZvDpPXN;Lr~i2M>P3F?DnI;RCx<Ujj^W3rfQtpp{&I5($ClLdWCnNvST~s?D&U#TifMU?h(gx`kRv&'
            'I^3=fh$zoH`CEi@>MZ7sYdiCZcKRS2=i#R!alRr6p{OrZS^Ze-'
            'f!Q(@m`RhUc?B(&%;p3B6Z=m@P&yG*t{5d~3IeGK!Pd}Z|!t>P}&M7Bqk;@5lg?~*t$X^^D|Cs-'
            'H@bby?!}dWg;X>uJvRN)B*ZBp2aZy13!QlT^M>>R)`)g6{pR6`THlR<*F;4w6?r?9Az<&U3Ujd~kaMO6{Bza+iMx'
            'dZOjS$>4#cF3hnIa;r3LuOPoD-q-n6MwmQ<pBU;D7g$X1${CG}0a-'
            '4*e<C&A<0r^AR4Fy=Eemuw;GF0in*yik6fR+9DN{I}*5QtQCg@=+BA|dvM%q`Y4;Z-'
            ';JT&pBQ2GlJ#b}DBfxakCO3teA>Ca*K4>EcuDo{&XA@w1o&AwIj`zwT~3?iT>+P7vcTOS)*>#$vX)33#X|yb%E~z'
            'rdJv}cQNw?Ejn7a%FBfnqbj#`MVgn@9_?rAT(C4af$H}iIO)jYPUUCMMidq!a`*KxRczdaZq_m<*7aV>N_u)-'
            '}H0Ee>Zlfq+<PP826*Yl_KiAk<FL7ybt@-%@ykL;PRX=wReb2xtd4#1{r@3diV-'
            '2oDp)n1XBbD?4G@UGo>=&z5y`nBms|c&$o@|<YF*z$1#!p=!!AFzc%s2F8+VG%fmG>xKR0#^WUDNt~v9h0CoJqq$'
            'Ke{>YTyD_#TyNIP&Dy{jdCe56^M6Cv5%xb7_$~l<k-'
            'vj`!ke{0dJ(~}O*MHxDHr&r0Paj0MA+>?^{jdi2w1PK6|{~gbKn;EjY`gnH5`3~Ow7DI-yn>b))8Vf2770MwlVIL'
            'V8uN6h?e=;buN(1gc5uhx#wv?tZW)sU#^H!In^|UI(tnCls(#SD&QZc7sV{+CBlKLmUMWkr9o``2Hc{Ui;d<$f_U'
            '~Ju&MKrM^3Y3=X-'
            'a@;<))}@IOe$;Q61GaJYizjwCw63ydR=J;18obS3BR0LlKowHT{8pA=lwN=!3wz7jgBy_y(FtDw!&)_R`qo;v~c7'
            '+Q-O8q1a2&#V>*r$D19j9d`$?_+iQl9Cx&+^rA*bOXG&W&<@?*8dtl;TQf#Vobc3ZG8b!$>pX2c6PI-'
            '2Tihv;<dKK1=#VbSm`T>l0z=<p}v63R>7j-Dj;Ws_r!R8@HpWV*AsZ+0?gAe_*#zWE4SE-'
            '>~1t5e9(vu3;lN_DHFLHxdlL}CH}LTUW<1ePm@2bLB0TPmFf3nQJ?Gm@}hwx?I(+}S!>)mhacAK)zDb=DCuA!N6F'
            'h$#x4GDKn^_TNp(F`_XrQ4_iSHKL^rvZ%tCDXG=_D+UWVLNBXD!4WvYqv*)8BzC_e4s35pat!#6x19AoJG>Ix2wg'
            '$jNtHWf<14V@q^QJ)`xSU?ltYSTZa37`Lzjltilfz`Q&$+3CbgAlouG=eurO-'
            '=`&@W6qSBlSoA+d796TcaGGGm|=`<ATR&PeK?Z-'
            'mz>n27U_;`l?)C4AVtfZ9b%#M~C5uv)?{U&&Exih6cfBB)uxDuOFs<-{0VeS$)-'
            'vXNyI=_iVC)c4>I(X+5nc<JmR*n@3npP^}?^fkWgXhx7EOs@W_BL;D(7UNQV$a%0YRn<}6!>M6d20g!o2Kfw_Hp-'
            '}#yd55#mYeSuqRb8)}5y~3)(o9y<3z9p84(Z^@@%_UW#3x}pjq)UY9bF&8gx`)|uOEXPAe9HN@s9%&GhRP0&sLMw'
            '^|NYT4@^k}Wk|r-c0>@I%Zfzk5}6>pK5ubfr-'
            '<$b=Q5eia@q2FsM&bu?&E*fl7ZAmC)8j2q$L@%_=z&{FdK^>hnnUUAEqd+y*j3Ybca%xUO&$~I9?}!y15;ztMP-R'
            'wz6+#?^A#f&!v5*K2S1qX|!27h~EK5OXxSLy)J){<i6QjERN0(*VT{^1+X;FevIFS))(<_T>AKkdmgD3!s?s>?Om'
            'B5z+OYAbtYDY=)T~Icv)})E|!iLdL_-'
            '!peC>gv#$>pZxv>9xdd@Hu@NGezNr8cczu|kbAW7gAz0JKQWx%>9bd20w*Cr2rg%^I08kpHuTS#VM+c|{J9+x*%?'
            'tR)Pd_|+nI9dT{Fsgs{Mr1H*_=NNwYtV}>Sip4AH!=mbf<!W(rgT`cDWuxQv_U7EHh6Kpz(ZuKX?k%*2Dk>py&lO'
            '^doRcy8V5VURifXcNl}ji2pmxLbSkaDONODEY2p=ceLUL>6meBBf85&dI46&y!?>yyIXuHrkgd2E6_nT(O+Fch1;'
            'H><p8#UyVflQ+BFuQ%cevQ#*6w2X&*gwq^)*Hg1rMtt<)Gifi2~nf!P0!nYLvCE1e_O!d4vgNPj#!JUo8&G=K8!O'
            '{z$N(Z#^B;35b#M*EBhDK1g5dQsD(<IV}s+?!WFzIt(}XVmR`O{kkowBrXA1#@idKV0&R=&Hi`*n{_YtRz9f|M{2'
            '~Ygz+SQf(~c#;3}f2T>e=2`GU}wpLJ9?q1u6w;Q`J9evH>yGM|b%7ZyrbBU|-'
            'MSV6ju50F#3)ma=j$K*j>QdY7pvd~di(>kYIdb4*<(p|PjrlO~AQ=?t)a(z(x<=s4Q}}(eYJe>R<`6e~n_9?Y!&I'
            '<M$Z{``yrjQYzyXf`s|J=zjGPg(FIHJBfHzHtRn59m$qVvWQT|n5i_~CVC2x6SZ1#7n+vIA(^2EH}RI_BVS=Rttc'
            'z+j*>+!EuY78bgOW3IKRNnqt9g98g;cjlk?rzP#DcYadw%6Pj`Yz;_$II&k<pttyix0rxO8qgKgMrGfQ3ElMS`cE'
            'j2@=R`lZc_%Y*&l!@Lb~RY%8w}JX9Adpnb#qH(qTjTeb8yUCd@FDQL}=Wv3$>HSw7D$#~}cAhg=7?Ic}~-'
            'Czy)=X@5_)Vc`?oNZxWiJ-jmxZW%z8%$;~mU=9Fp~Hr=r}04aVQGW@5(-'
            'a)S=Zt&0JZ=~!_ga5k9og}xf!7ZYt}Q^ZgMZtf5YH{0l~)2&|;BOg|sOSgDnhU7#ipW>D`B~o^F}7!O13f>1%msE'
            'C`K~vkj8y-!>(xxtZ-m-vBg&3nj9BQBq6Ohd9nwp1fY=t73x}#SrOP2KUWZZ?Glbo}K!tBEgkx_dJ-'
            'med;H^b`$tqFAG#eGNse9q=od-GR*|QM6^TtA2j{-'
            'LNyD7lAr*ImgsjT1y&%jiR;F}OI%zlSC1rhjs&(#`$BEd*#`9^Gg$Qc0+we`lo3sJV{>Uh3dhDtnAjbXt$!(Jz@R'
            '9L{%b>M8Mwwi$rj4qIepD@mme@r8D%t64uWgBMka2k*dVj9p*8lj9tu-zy^yiI5$odEh(AhLu{`iu?|w=SUSKzs&'
            'Ia4-kfdi$uJt`0$LNSgDN8YeZB`>)Od6@ogfUQ8J#+_p^6VG}`EyE)mHXo_2Y-'
            'Hk@bXEn8f7k%X3jw7EpP2Y>u{6S^EqI6QB=6t%d$d0iS*XtEj#WK-KUpzA{K;ecGiekq6{lUfzMZy<psX<!g0#EP'
            'Bi56$)*C1gRp;M^l0GS14MdcUr_0(1EWuiMC}W`hKjL0x;X#$KpchW)GF0dW3+EK1wOv2n<d6F(xUHJy=i>hke&F'
            'f^p9`l4=4aQPqrm7Su`<zTZd8$JV)24#kD2Qi9Oh-8(E9m3QD!=--Zo|`9lp@{5v-Ccv&wM2>8xt($XQEv-'
            'T5>R593*ozGa8JQG@qIu?Q3&e15XcwfR~90U`lky@;LE0tv!`PpVDT*Jr`K`$jqcW5ZzGbbnJU$gsCvmzbKc+jF5'
            '^Pt(Om<$edrfgu=T%$y}-q5u0i6^8H0J7nATGk-'
            '?rS<ttPqY@;a$+PYX9BMT43wzVYoVDIXOSq}u{b4XUOhKC)I^BQJUtLQN^Ybmq3(b20iZrk4iveOOWF(2n0pD*J?'
            '6w{DVakkT&<0BNN>GUBWo=mui^$5g&Z9*_`zQ1sJo|wc1Wbhfc9Z`Ig%ioCfV7M$KC~u2oRLiGrg!$WQyP(vYT)('
            ';C1;pEVReLZ5UwtE(EsVjc^x~^<tr(RUqp;AuFs@)bNuz0+dHClPHwg3@OvIb#bZBgsqBN?4&zFZb!<~DS0M6|5B'
            'r+MCLu?Bkf!NxvT$ah-|h!SFE%B603{D8^i|$h43jdcne@z<-'
            'KhOF;XxIq0E$yH${%(;ZS@3*=9Qu7HH%Nx=0~LN=60cwCY@FC=<3Z6(7*)5FdNQhiY?Ktja07-x-'
            '!CcJ_tyk#^Jf?2MO+UsCzvD0Ak5F2hj#p0(=LXtlUu(R!G98Z;${*nROD4xB+~Y1-'
            'Z?y)cD`C_5Go=?~`_fj`7EBHUH=cBwgRSNUrZ#c14ZOE=dL!>-'
            '*yg)N#JTb!k86NHfZl@A5hmPZ!~e;>84RUMHY$2cW(U<os8sb!;t7XFz~Hmrz$%Pmg3V1XDYnX4@!V$LR?bLGzvI'
            'r)(>x^lB7EC{g{a2bwP#k^Q0<fXepO^9-'
            'WSAOqj=rsm+3>_xXB^<t8q7&ZbS$Vzzo@#NeZ`Ef#K<}CfU=YlMhuVJA%<h)|l8p<hSqL4(JFTGZzSS<;sKE@(S('
            'I~QEy0^+EmuRB5KVp0LMwB7(E{xy$5-nSXJ$Ux-<y=p_TZ<3ZF;K}NbF|IL#~~}rI$6j)2-'
            'KlgpEVrw12Kf=|dU?Mlay$biBGzsZw)9hVlj%9-aL1UX_bQvf5OZR}SfUP~w)W80(-'
            'KT)<(4NNc$|1s+j_`|N>6aT4T&OP!UgwtOKK=QEbpRbJ?xw{zPFWP7HM%&jK{J%#}C&`u<*P4xv)88{jc@hL7vOm'
            '6sms%K`TsmrOcBxZ{W*4{&Zn3&q2;0jWjtzl&sTQWlMVr<kDejbgaDSGiQiDz@rUrHze{B~L7c`CP`+}HpFKKH>b'
            '>PC>i*i<;45lSE#A6HJHEvQX*&mS}#buDUDEQ<+Xu0~}k*NlCc#a^dg+;}pZvEX4fFrTwlh9d~|$P@R;wmu5%c|?'
            'cAhNlgRk{uv0sej9}YP_fp2;I9O&5uKNMNr*FdMatqHSIgz6>G5tvI(YUA8xvC?sX&{Aan<%(jdGrLfDR#@Vs)D9'
            '(3OZ4^jX_@YZU+w{(`LS@`hD%YcZNek&B^iX4YFq&WII<*(>Q=8UX3AZrd4SvLmZWwx2FhhK^9XU=P>p5lPJHvUJ'
            '4`3&utr+ou3`!;y?#sB&n)Q4#Iz||X@8N{)k-;n4b>Q^OvFAd-FePkkdxNH<`Y+u}c=V1zV@eXO<Kek{;K8Jn5w|'
            '89q%zD|yv)ZY}@*ZYOg|)O_cL``)Fy@bf+ktk=b#7xtGn9|K44X6``WE$ILl&sv4NJN9pgJmmG=|LXSezJr8#C~3'
            'rJUJRlVx*Jn@g0!K|qmcE*V!xYn_$TwW3R6!8$&O^u?^h(jVEbq%=?aK>x#vPt`-JJZ}X&gdRt-'
            '$A)f77&DQDU~nM^qB_8e^~6dfkp|E~zXvR3)s3-9!-~rKB*QOOfibnzX`*@NSjxpw-'
            '>}Ba0D#mn_)t=tyOql4<#HjPxuw46_IaL70N2Z^Q0Kkpoa87F9~W|rM>RW$bd2gIP=E=SlL)6_S{Mal8aF-'
            '=FxrAOnmS754nV-$%NU6JrRADwKoS=G)BvU$N&CSW9D;jux<)j*IyZD=4m-BAJ;Hj>eF-}cEqFjUHesZa`-'
            'LaREIBLY<c_WL94P*r)RETt+!^-'
            'XQMR0c(1EZ_rvsxmOS0PvJw?Ex!u%0INz)<TKN_=X|Le)>ywKsGM~@4@TOOHxs{}Zv7nAB-s2q7u3I-'
            'V00sK=_o>#eruTl}>?iwz9j-'
            '6gjlx)~M1rqUu#yAEb3k8X<w^f>w@TA!mJ`GU|jbR)?%@2X;;K_0FaQET22~W9$nBZ7Qv__F20{_#o$ze9OJW2?b'
            'lWX*?(Xi7X<DV?mk-'
            '!LXT)GoCMKJSEJf~iVtADZ}YYqBQ02P}F!Be3fBb>@E;DD4D0gw#uV<=K9=pb7gq{izJ#+Q)|LS@6*tk9P16Q7**'
            '?oH_Ra5x%=FBmwCfu)UnQ%q(yHKGVWQp%haq#6fM!Q&yr00m?Pcs%WX4(qt6XFeK@&8^2Y{uVaaBYu|qrOxv?+9H'
            '+Vz`q>4U5mgAmCDVnMU5>+$yG*Z3y5K-'
            '5c^|R!gCQ3jXEr^b795uWpt@WDK3}mYdM;!LlHZBi|uhgqKSDTa`SP9EIn8!7?QUpc7oTUE|y+Y*(j$shfNn##8{'
            '?$U8~3E)3Q$?ei<Xvi?x}k2YqukXP4!gyvFoZsZG{0b~Ae2e^iO|d}XtiQ4KFKo99%-'
            '+yj*WO=jXbuBMw3#mBVX2u`s8Ls}aiim7ZyTaeu*-'
            'IGfJVquMwlI416eamh;S+^Y3+#iKPt@tAOIys7w*@!~8&x?xm9EdOFN?^>6z!<r#zbndgbG^}X{wGHo1w8UcEZ5g'
            'DcGgHj;=Q7rKme^Ao3lkZRk^Or<V7^NbPgwDpAvped!Fc^g)aGtX>!BsG+tQwJM6k_e#ReL-'
            '&Hw+A9%|<6K{$8Rw^tNa||<l>&UfF#D9xt(=r;$wURMM&MZyyef)!YWy0@tp8nv$lN{ueIRFwZu+sJ1Fs7F?Z#Z@'
            'n(}TetsNq<}^<$C~pO-Np%}su}xPDf>4}n~P+ZwCgg#jB1=D_O3fjbmw=QzptfS@(B>Be85p(+gy(Lhbk?P3AZ_7'
            '_wm36Dbie8jJ~Sec|{NvR^lBpSQXdlzZnMD#((3ldKG?leimoDw2J>$0A07KI?#f353F<O?Xu2K9GzJw=`|U-'
            'CY_sILSuUQX~)mkh0Vz3r@eS_{H=kX8YMo9h^#Z^|+EKH^qC<5DxP-'
            '?)LfC9WB5yun1Q$RXy*k#yODgC+_*@VP&z)qc$MaN9WneO>4pIS<V7v6;EEllqW5m^j)sr4)VO#$Y@HDPs)JBuq0'
            'npJ0|H{7ZNa*sg0*kSR(`LI_CpdcD)EuNOrkuCVE>bhScVJbGYYQm*y2Wq1~9rf@b0xsXuA5B<(d&#e0|?C`?(bs'
            '=Ku;(ij&R024H0wH|FFBXK9OWzj2!t{_ZWO=p$UP9hS1j^)mf|hCkqsZ?l9P)M~<cK^(!a&6G9TzWFD~Y99#D8eY'
            'aiio7I>(^Rg8t6B!1CKVuPJj)uHF{Mr46Zq`%c5#EAZs_qCBhL!AmT+)~r$Tt*<H|4C)M%$M^0fJWqS@OCyG}!e5'
            '@zZ->Em4IiR`PINZGa9_iXM-JEXWmjXE4h3S2e0{wvB4bM^Sc7*hiU$0Mg_#hDVG(f+s<XIC7W$mPA{@|ukzg_zI'
            'yYbiMdmR3>enLMQB@QwrbwXz?yDI`*LgR*<?NRNYbT`2Wj7uEcfbYHa7I*vIW#gv6?i;27aTp!D71yS2isY=0<Ie'
            'X``2P-'
            'EeHQg`v$AU2=b6$R>fsqVah{hQ?NOPC@mM0X)#RyhX|!nAO6q({(tdPVoUp}G`p;dF?z1TriQEZ?PTY#yE}h4y$3'
            'zK`NmUVFz59Gc}KMeG#UeoRBgl-njHJ(7{9g>iZcAwNI675<s6#7XKJZ2AsEIsWFp^?(x4e_oaU#R|NnDY08@o?C'
            '1NGXx;|$jqhePD@(B&wJJjowV;|+4GB}Qco&WZew?iCpWGy<mm+;ptlNo)AieMl-eS~|G_Vl^Bz|br)s>Vwpsfp3'
            'a#=}i02E@`siKg;ZL~H^&E52sR^M)7E6+SK-k{66IjGj?KaNk9DYv>T}t39P+48(uKBO_zqP|HbyTjC}}A16-;-'
            'wg#M@eeo!anWo$_cbAcyn|L}+m&T=M%dE6$JjpA9mg?nkCrc`Z+*uAIx%6?*U>;d<yIp)IUB*v%U_JkDB8d~T(EP'
            'VN80pLELyZ|zjfPXBmDnT!w+H`+E}RW9LhNILyzd`5$!aK3i!OL7r03hJLz!~AN#T#uh)o${2mccFZwHQUm4hsY6'
            '^ocs0p`(ni!tI_E?UwCE)ZJQ)2{v@SP9`z09_VQ-ZE)Y5{)B-'
            'QXz(Qz8P8du%1xJ$l}N)Gep2^G1Bs`D~5Wfi1P14LdwLr_ve7&f>g<uQwLsAiid3bC8%^)h;rJEo2%S!guX`*_0h'
            'OO*Huk*#FEU+!^-oRsVLHBHDTT1W9#*89e=6I{9ArtlZYhImz}(ri8}$s<kg#q%5b_Xqz3H-'
            'gbDdg3sgOB1$O0ENY5;HvL1y47xrVdfD=YA@)%xJd)C=&SIs5uZW#Bg0Yx|M=xaaE4mP#luPpy##=Q6a-'
            '*?jO}x4bt06&XFPix6f&U5{pv3t;BOt9@wlX@%=lLbpwK4ru*w7+J#yh738<?)B7{k*K%=++;-'
            '|b6=JsbXU|Lwuff1GB_>yNZ(V67=8bGY;1dUGH+Z(ij;KRf&-'
            'e|2>7?A6Qs;Q6zIV@l|M!;kA6L=05zbGBRLc!%N}T}L2Q>Mzv5iN7*&GgHz`I^Fr3?5_Tz?);bPj+sQQ-'
            's*T9Ycw?+`QLD5_E(xT)STuI{V)glAvk`GDcUxXAK{zaTVw&=&mz=xG`RKX7NxLmNFSJUu6K)sjYI-'
            '?C+t*{Zor61!{(#tp}#f8IF)Jtmw-gM?tMf5)Us#7!YGp#{E3)+Zq7#g^1Q+@@x0m0LA0Vlpc@+$&gu_@&GeW21B'
            'AMBAo2K5Mqv6U-2OHEQxh_{;)K~me`ECBAVK<GkWDXgOXaAhdS+ElDoR3kqkD~v@jPhU+R-'
            '1haa^VgiakHbK#d6mhqG^R<3KbM(6!4;+Kuk^b}!jM2WHXf)T4gxu1G=@BlT<L?baf#st5VkHSA9}6bM10VYr2ZY'
            '2oNZr5+0Ddq_{gFD=~?ajdp45B+4QD#AIFe_JckdA)?|g#S&!K*BI7G`^}a<7QXmsLF$w4oB}XLI*`p`Jr=#TU=t'
            'p`VS#F;=?vcntFq&Kb9-0Gc$@GpngDh4Jb4M21W#^kfkl#2!0z9MN6{|mAg5H5&{ro)c2q)!!Ztm4-h-'
            'V8{b1M<;@JNm$`aFt>ECB1tFzG5hNv~jL^&;pU%%r<Eu?77d=Y8-rXG-'
            'iCYZ}^JN7;sh=IP|HG!#8IPtq*^&H@GycA6)h~q9>uw&HjquyA-OJc?1{VOP`x6c7?ZcdF-'
            ')r4_KlU(cKkIs#FN*iYqS;nYV&+N#mU#IbM-'
            'h87RAQz&jA9|>gk;!Pv+MP8YVCYot`{;Y&}NkHpvzM8j3}o!jDLc|r#2_;>$J2=+y2dXJ>@#hWgB{AD^VO#XW?zF'
            'Ou?%D6J?KcNA6N}5|zuFDf$KNJ51p>aN(Q>mX{Emi8f1S)Zou{7$Mpjzy4-'
            '702)dXF})}kGoZSNQys^F?H`Ngsppxf{WQ&Cvks^jG*jGBkn-$1J#y}ZAOCF+&_uME-'
            'rPY7AY0N~wQs{{XinrrYqnnM==8?+If6{QbfHwI23=P=_IQWrlv_R;`r#Nx=fLMA5=2T_1M#{gH|Dkb-Rd?CcQG+'
            'et|$`RW?ZOHyqS@H$>6nw;2?&+1IOh`FQ1(c>tMe$<MkA)!BG5;(z!lG5qCre(1tQQVr>l*<CGgWvTL@h3!t2_SE'
            '+l5%VaJ7z;<;6gDd0-'
            '_L3W8Cd3WF*{K2+cGx==@reV(P<`nFTT#uJ;)fWYG!tYIY{kb#*>)F^Mxm^4`lF37`wqz)gxP_8`%h1IC1pxt5Mp'
            'wsPP0l%ynWT{?d~bX+sQ%b>A-'
            'nZ*KtlKl;<Y#Z?%GCUIq<u9#T^^Pj48|m?xH2bnCw@eUuB9ULot36+7fF@(~NCbcu^qF_~RUR~aWeL3AOX8irCrG'
            '3+z_7UG-jK5`W@y++ppBx7V<yL-v-;jW8hj{0BtQtf7bxtwsA^^l(oee?ColkXK0N<xqg!a>UhZR$uBtU>j5=iA-'
            'AQ}(}*#t@>@isRtq#D;lH$I_<v#dsogwx@P1%eFP^eAyT)Gb!_}ZSb+PfV+8hhbjRZTN5zXxr&9&#>o?1`;bN@i%'
            '>kvv2(5ngW<d4dVevwJe#4{D4Zz}dH!FZWaxbQ9+ftt>KVx!?!nIr&O%C(k+SLQX;eZ#R^qhvlOfy1+UGWgo~z{@'
            'xeQ?wW8c=#&Ul#F-!K3MwKV|Ja?Vl0u7-'
            'z~oUAWa_2!)ODSHV1@s6}DXOJrelH%Mu7{4vwY~xTq%R??Q{Wm2iR<+HbvDen1&{+6KbT@Sz<@tHBipY0b8zkBpW'
            'O@n^c-PsFS{c1?OFR^-'
            'uUk9U)ro9tzxqm=6k|EBkN9eO6)((Qv?!Mez;DqW=CZxX0y3hkoaP(bNAe7|l@L|l!Pbe*g$~<h3b;ZB$H-'
            'bz0V6px+!$KV651+%g-'
            '}W&1!`l^ES8?AJ!>_;FgFGXxRtfZ&qVwkWlj?6JWS@^BO#Mol@Hc#pLO;$J;stW(yLTG>LOxhqVD1u#Uc|_*n~u$'
            'e@(G?UvSz#F<e=_uMzb1W{nw+MYI?YJ9G%VA_d+!`KiIoC=&Lf+#$Lv6Rj>q9>XtGO&XEzK}241urDT^<`)=)7`d'
            'p*ohi;oBaL}4<H*u_VB5qtY`?)Zhuf(ukE2Ms&H1%413LfKUPZ&fVY8?KrtY|*scuyQx-XJ9RC^IHX;L*MdSSkPQ'
            'B<4zLTPR~mGUzzE(65^aZWx_qwEV5QA$kFH{t_FoI+#(vRL2}iN!CM6u!8@sPD6DpkAa1e@3OcnWvIYkjCpfupIQ'
            '&{$!3pk}G6U<ki}e=9(>eCD$Rw3d3WsK&9g#O9yF02ozkj*5JI+8;|lO%$%~I<S4*4rvP(ju62~y%692+pm|V^f4'
            'a+9()&P<<;DW_VWK`)jF3z`%nB!3t2l2ix9XmED1^&BUXKfX!m^~vi7Eva9~|koFu~bMrVBw|2}Er_s@6cw=z#=Z'
            'fDSg%_3-dAKmP-sn}1Cu8w>BMWENUHc%_6S$##1vf@C#G5>|csIs5u7qw8`UTdfuUcOaMq&iIK6PDw(W1?D&q1aA'
            'VgvD(1nNM>JRA-%+;AuSTmy-kt|iO8xVl1XdT;!x(6QCKoP(Av#a!p{giA&SZKJT2R$0{^52-'
            'F&&vlN<H0dPoH=C)|Tk_jqNC$K@c<K|c;T!X29xpj!*5VY(5Pi$yTOO(4R@b&Qn<!U2j-'
            '0W(9EEeI>}60t%I`#If4?qGqip4;zjG!_7n(S^j{QX1a1SwtOGIG;h|ud43y4D6Djl|4g4jcx@Abp{HJ93!uxv7u'
            's_<jIJtr#*C)5ifyX-&cp9+|_-=j}MBujR*(S5MsKr8+n6z!c&L-'
            '7dzcLa$wZ0%?&v7mXI>mr>gph9tl;cbQuCa_B6t7L&p1TU&Ro4)_@3LI#(8bihHdrCO$jM)dIAp)P?}9*4`mUM>i'
            'uC{Q5eedjFeU+nbQ8)bepB;#^(zz8>t}ej>~Rv1lV{9B_Q}h{EW&CRPi}yJwpNc+<)n@M(R{0{Iz&&Sx={b6mKvD'
            '1b~MVw7F%>A%)R7TX=vf(~V0@9qZ7C;#LwWzO1tK$3ff3?B?fVfJ?D`dFu~Se#?0b5|b+uRcy*AMfZDrZKj|m*0j'
            'Kom+2Cm*bc27WUG@|2*6c`Q{kTTHd_2vzGg_H(G#RWj1<$k%*chtgU%pfQ(XBJHpR~?)TYbHBNr27UjEwv*rUuMr'
            'Xvba%TJ@F}=EmnJ5=L;zT|GpGAGetQ=YeMc^-yLd?TiR%4I<$YE~Dyb(ufB|$e^-'
            '7(tLL>wIIPm@)@m{&D#YtXCOgQT+ZL)NXE?{FV|!K>ZUEFilHLWF0=OgsDNznwIg!3*O%MwjqJ*s%UYK7L*WCd<c'
            '<^f79gt<VjEO}XO8M~6zNTb_4v^hkwowLUq3-~}~8M!N;iTn*&Yo$dn*+H$P@<r)=R*N8>C^M3K~t-'
            ')#DywQ;O*pp#y!&nt%xHc9UslSdbLK273HC%|GjAy1$gOZM(nXLFJM_nPw5el=wnS56tK*xY>?5QmxKmM@E(n0p3'
            'qHe9dcG!oti$i1-ZD)CF2C&RL;P@zQZlWeT86DvFySpGu7*F>o0&C~(lg1RRv9+ovvt&`%?>0-rhDO0Y>+-'
            'BzU_vx$Lc?p|4n@50*#_tpn()xxhp)2SmYY3KJY2(U+-fRq^QGR-r&&`Go3Psa>?d<-'
            '?ntAdU7DqsCOw*42}!#{v*;@QnZ?LiXyUEq{npw0DpNi}3G%5GA+7rfNt*E++M?9Bi~gehoCRP0aJQ%0;K4V$kwN'
            'b5n*<}Y^te(XylOS>gWW-x05`2FnK(Iap=tVV-;us*6-O^B-'
            '%8B0L4@QAM3Ac8EgU9)Z#qm`8I`V}fz0!eZf|D^>ZMJOM$1K!X4Wo>w%~bB?!!xG!H0e)XGNr<xucm1`72V55eKZ'
            '>Qn=8Cf2?@vvtr8m7dUxpV)-oG-LLo#D>2-'
            'Ow_Jv>PqqMZumwJL8iCS7s(q+C3jQF5bTS_*oVnVdjb}EF>6B*;8`e3uH$b|a7NH~#P7b1JeO>|CWJX8ch<Ukc);'
            'l!P4ktRN(EqZ+jLhsp!V_p)&6cm(8WZXX?}wogK~8BNhFK)<58KmOPlf%p^&Q=gY1PqRaf7iR$-'
            'k1n+Y#Qwlz@<$wRzLbOi9+>Ths)@{;J-ZOdBEpw^9S*Sxy&N`up`7-'
            '4`e&{YwJ$!Dd}E<PE#^yQ;nd{5W?`Pt@6r9HM)0ggiOcnalH`p}1VkgU$_(H4HI+)yLsjg_-ni+|NBZVn9P<m0DR'
            '?VsbPzkI8^8)H5g8ci?CP)o}Z=fhnV@t(nR2T0@Svjxru4ub<;I_QH&r_su_GdePi$ZATQFe_{JrR5N13*gyiT1+'
            'V|In?=@RH;OL9Zbm@If_@74hK^RZz%oV8@ZtgK96tOe*aZK(-'
            'mJ&)9#n8WhxAjvtQQNXIowmM`9*Y$b2Ws1))~N4eAHB@)NWm$aVh6~MkVK)xFs4miWRRafX?Ptsa<Avte3s|QSwI'
            'B4Hk4>)eX>sM)y`8R-{%JYsWpRa%jO_X|AlEO%@4%RsB=<>2*U*6!7+M>=U?sB%C1Z9|Y{-'
            'S2xl`PPu<0|8?sXY~e!p%q+?cXb3o!+L;kCkIq+Qi!|Ze8*bcNB~)?mix&t+rUjnH$nuR9Q@50<rlm^;ikp8Tvr}'
            'O8+uNSlbGgm%1iRFY<Wcm~KIqJE^g?&pt3sRPshuovhTmn>!XV}j8Re}b;R!M?nKidEFqXeC8%2+^XcKUc>_`IFC'
            '#f2-7^W@GNeAWRT%&J_JA7Z91b$|wwU{}-'
            'g=)BdY6Bxfsy!pyR_4WEh9Z?Co_td2UoBbM{7h}4)ZjMu8o9BSgbckDh(SFe2kUuiLg$g+R!^u#bxaCYYC;hw7zS'
            '7jJ9=Je8r#l-9URI(_W04??f5%UKqkfhwGywd%G#&M0*6)#>JT9eTH@p9ijJrQp}189mH5ZZ&4-'
            'L1hi)iMkY(a&#<EM=nm6kcUWVQpbt_j_^p-H+8o457o|2yKCc#<fN{*m1o;+pPg)bs?-{s*u6B0-'
            'Cnq+=NUF2NUP;Pvn;Z;blPg=iAsaf4nCO!G6r)*Yk4e1Mo^|d46JQYwSrRVQf0e7|#CfZrt)ICH&BF2T!NtZ)BG1'
            ')dy@NgN>Y_G2)BKPQP0W#PIQnujSCMzLEv-'
            '?=l5I*|M(;E`SL|>H(A^^d8I=tzDZSv}VX|Nn$0@8i?B|1lEX*;iFu2+!Uu<#Ye47Zsi#>TM0D8?3zn*rghzw0TV'
            'j!n^{r|rqA7M8{Zz%Y&*il^hr`{D`B8qhf%Z>Ti%1PI=uAhuCdI&7eq68r#sfgrI@q;Ucve!0Oqa_ft|<Ou%TRz_'
            'iMh^7D#qu=;^QBM%>|82Y*_qFcQ1C0PEgPsbT$Mxk|{ipf^^mz&pdLr=p_4BeS4re7u60eUo&Be#)SB(8*z@7eUT'
            'zpspo!m4Sc`+8jBO!f>0V1JWF}?&RyPA|{mj@5Wy8#_TL_5Zq3OJv`(qvsiao2KPXUL^Auh-'
            ')P4TA&OZhUZ%KY_u1YKoUM)Ds~p`Q(8nMnqK<PpnTLjoo$$N8_gMGmgtvb76tP0*+L*lxJ+W!wTwkepY`_?IezbR'
            'b33c&#&epJrXhsct3XC^E9D$g*7r|29Kal%xo>lmzl1lUyo*bQDA&p{~opqPR*D`JDQcR;-'
            'kX{fE<7ZKgLC9uiva(QA)sTT>~%Jjvh<+fQEwpqpMXJ-'
            '2)R%H$dkvt)rX0pH$NrSVenD&Z!568wVRBa?NtC1s?dhQ`u>?b_fC5aC2$#Qsehik76+=i;}2{Q~@0ov{l5!D{F<'
            'JpFIbHrtxvC_&95I4lip>=!La+gDI@pvZoyOqrh$ay|v7q<GFe=pX?w$jW27sy;#X9Li0XO-'
            '|g^hogm$dZ~G(AA(YA>cItNrw+L<ALd9<wx$mOkM|(AUv2`o?i9u8}S}63}9*%%|U%f);<~&&h1~K2N=m54+A^NZ'
            'c`b#2A>~9koz<xVGcJaqh&qScR`YqVgoE@lt+w{gG5gbZ9KY=04*D2VQUkr%?@^uj-'
            '#h;(}NJ^9dtha}8U!}kp^dun{EPARZ3fgLGP$-Sq-HbtA9?Cn~gIXwwZv&Dwdp^Pv<R`+rvoWacadiwpYT=*I3?w'
            'A{P}05lW+P@6-O#kOklcS(v@2CDI@&kywFI3~Razz%2`sxVqkYsexkgL{GrW=Re3>b2PbW+0M;BWY3-'
            'n=&?9O{u4XSnrTcO&o90?_`F8d&BL`+uP=Z@mE7w@G1t^({)ROZqjBto;Y$mnQwIyJ1on!CUA_SGOQW?gYqGfSTM'
            'Bnj2kfJkJ{ntB0T11eB(F?zDDXu23?5`W_^z2nHtE&82x=62&v`WW!zI8S+)ZrroPwDxT{>kH$ZsP;UkY9drhy0Y'
            'eo;9W%S`$P!gT+5dVKzGivZ{AvC$$jsxv&+C|gR1$gTQTcP&{}mImM)c5C~*oZRp_Qsjx);Gje!A<$t{AJ+V>V_f'
            '>oLjw0qfBCW3A)iow-'
            '8iDghH95T{v4WmzK&(qeoVLZ@r7*y=_4QKT0Czv$D@HDU90g_7FTr^$DX}}Ak!?Y(Cy`_ckV+`b-'
            'roRpgd7H7Ok+bx5%IWRnp;lcsPxuoq-PTg|St6b#R?Q-'
            'THQh^ozdKT~Hham}_*eZ7{`GM8c6?q0KyRGbD0x7^DaN*gG2IR_;u1pHFij*=87uJfD3QB2(FKoZCP85lXa`^IcO'
            '*XGesVeaFzi^^C^5nt%5`zMNB=GJC&$!F-CAVNzST+4=4^3>-'
            'Z#cJFw#ZTW$X5V;fCXoWw}QJkDe>Nhf94VZ0K`xlF}(V+Nkd5a^?6u$04|1<tU<JDAPVMivj17Pk#cipsfy|k7a@'
            '$Pf6w}9#U+d8>Ky+2&8>D#<lFVty5?=lm~$4eGu_g2pZ0#1$8~?Ry$29+17WR6q?zn!(`a4!AaOiZVisy9&&B?`*'
            ';h$)+*qGs%fEM6SPfc!O+-'
            'FgW0w*s<Ffi!Yd0k*)+q8de##09^AoL_Z0s`?B62XU9UmB;>T1Ja+ofw^R%;zlpKeR)K8iA@#O?_mSo{k92rgwYD'
            'kR3ESjyt6j~gqt~E&oZHf>OmTUCNjFdF(=_=IT7oy}bFV-'
            '5Yb%3)~F?l!W92)gCL7+yU*@wR$v~S8~{I@_NWt(q;{!1-_f^F5$+B1xFiwtezL-'
            '#hwB~~to++x+f;#eVMK~ku1Au#k39=7Gv`|$0(I$DQ1vPyjS>fe%a!tzm1yW3@*Ey7|^zcE@d&N|wCydG>GL7=4V'
            'bV30S$>fQQA+V?;xy0X*R!Al!XTw}Sj?}9TV7y%DyAn+fYt6-eqS!u-'
            'CQ#9yquerU&7DGiGc3UD3DzR0XcGKIcvkmyR8LB;)*+vmpnu<8bT485Kz_b~Q8`}}#}{?W#oQe!PsNCut0#@yf`9'
            'MDY`0K)soMhV-'
            'z?i%{PwFD<*K9~r5!WMW}#26wux@EuYqZc9p6FAGY=ev^1g_hh<&NAnk7S(=tQQ>qZN^MMt#bHU1bs!*~(sWAZMG'
            'yw0OX@_>qv0$2KuH8l!}RU=ax<ussOltb%IC^+VODabkzPV7`KStR~etQb^GcrrlH+iQoRPxLmC6k6IskX=sM5KT'
            'm4`1>dX3oNVwJjw43v93cKyS<K-bS-'
            '?ASW=2WIR65)IefThm*ak~whsJeLioYF0)Hhf$$j%vTVmD)#E*Fz&aRCTgtOD_i!7l5%UYwN6K27nlYDmS=cRlOw'
            'MYJ%Iv8<-f<pmB>qd}7)U-^KvRMmAmfGOVvCoN>O?mR-'
            '(V@RAU=hRqVq{1*u9%ykXKSHxRnB4vnYfrD(C>PdFcw)AyJKL=8D2T>{&@7nVvBNg?kv6K{WG<p+wCz-'
            ';_srn#)F|5~HDk9mtM3-'
            'H(Ms*ZDOAy8IdkhI;M8s;?=%t&6C1B?5e9nkdxJiAA?#7!dL3GXi`|iBT8W>S%T|lTE~eLTvg5fHe-{jP+3Qs0n-'
            '1>Q*8U-'
            'V`aYX@AveMc=<lX>XW@X8W+xO#r)n9g?1et_t~h+zHX+9cf_6){P>sRjzgX4a?U{e+#pZL<$m_&E4pp8mt9Xmfl!'
            '{N2NW&V5aGU6GJfq?n`5IuOQzNMt`3M#tCQ~leN{OL%8q%c0wWX<&^#xp%%gHr~v@-'
            'W8FH48&!Qbq1+&j{2HM!!w>={c#w+A_tuD7oInPGATeznOFE4aemeJOfxwblGl%|)CXE<>^d^aBVa<}N}eDQk=|5'
            'KQSbHw?#PS`*6c3adkM-)`af90-'
            '_6W0F0y0<afHK74gd>E=dO^0`s+GhSo*cdY#RAn44j4$DYPggI1IL&nFjdD2U{9dpt3-'
            'E)m3+X_1*P*^sVNTn$<EK7cNoE!M#nDO1<gGp&hET)sWz!+*w6?Gb6bV?m&5nC!uQnM%bB<I>zKs7##+qeHr7TVL'
            '50s(`nC{->3j?WkM8J4C|-y0CnZ@)_Y$a67Be*nq_%Z?7h3S<?ys=KPp=mBqRrj-'
            '<T3j4B%CSHr`{4SNWx1p=}yGS;t2<y@2aw*a`;&oe4WoxESJBpYcz5D^6Y)lu8K6Hy~tf^V7N|E63BS@<syKDL5?'
            '2dt}qKM~VkeUW!d4Y^VFO_|eul!_2g+Bf8EK02H2Mb?;#8D8tWaFZh!@vF6ldu>WhtVfRjY{buhC?Ea@54}(6O^A'
            '(5kAD!EqQ~vF2CDPcDFQ|TlDRBn!NADSaEgDiVr|pn>M8vrw>IF>mjvmDRrzB+HZ>arlCTuHQXQ4T_iLWU4K-'
            '3qJCQ};&xksM}tm`t&S*`K|pOd<f1dg&AqJGPcfUWc%uY4=#w8I#Pol^uTV9ZM8#sOMY+q|pbI(Gzis;1rk&!eX6'
            'ekRBfQ`Y;}bjkjyD``QF~fT1^}&Q0o?Qu?l*>ti-Nm+{j6%CpNp90^9hFlh@k6mW{JBLAvEj2KBKzWt(69W5?>-'
            '0Y?O*cx(#$%6XQE2RX~%h)zZD_;fvk#?ixeOoW^FEt)9hVy?$d%Ir~FL1zERx*=MRa8_&UPl#rHM`i`QP?mjyz^V'
            '%4<Z~tjl=+y{~NjW_1wySTMYDTBG3S{;kvv9Fmlh>DA4`XLHR}`WbqbNzU!#ea1oF2}V)exeR@e5-'
            '^)}~by_7};&qjZl_rd_Dqs3Db1sE8FaS5%8*QBSEXs7UA!S5XXxSJ+HCbAkUhm@a+>;Qei{P2RUMynP5>E?*<m+S'
            'DbO?3d95*e>Z`kQ#OR(rlOo0!^*x?18J#vE?7hdr85mo$WFY+vL20Ar9@y^xgXP7(}9qN0PEnFwU?5=Gj&SvQieA'
            '8++ls_+;#e6E*;dDc|*9w~qjO3Uc(OeeK_9;N7NPCjLm3Yw`5!#}Ozq0!<nLh7&;Z>jpSX{7dIkH(#SaVbPalLPg'
            'K1Jh{{ls~Bg>A4Cb0q`V-9CAUHSBB68!C%=Msd~-'
            'HjrEmZ9VCO$3JAd8X`NKHhIlYG{k*5?^Vy`TdDGF0)m)a%S(;FHV5adfjj4y8uUO;Kk#>?3}b)aI@Z2vrPLE&}sU'
            'es;Be}pq(0c>d0{Oy5aR;Ukxr7Awaiy<$rc#c%y;t*OIoRN|z6+9ka)L8mwqUCksRCG9`EQ`$C0k)U`p+wW9jFUu'
            'H77ZAzq>7KWn3wenbULs-'
            '^_3)kUTh<PpoJPP$I4(P!5@pO7y_Oa34BJ!9mSrXzTh9X`3(<k7HJTZVX>5;GC)9lRb1BZiyY|n`r3oH^Y@-'
            '9y@!e(;7|!x-_TWJ%m`Rarhj#T#>%zSj#6cAQaxHl-<^rw;5_GN6i?v~i$!!(K3c4S+kbUQ-CMOP-iT%v!@(ebb9'
            'nUX%}M_J@Z}FDKjudVCntw*Uh<{F=M$x8?w0=NugzD(xA%5V|2X{P-'
            'mkNJ_}}ASXJ2K1{BQi<dl`IqTO6KJ6a4#+B2(WgrJj5@f8Ffvo_z!V{q@=O*YxzO41W8+(n02~<m6TU(+iBe634W'
            'cJQ(j5-'
            '!iw6UOInI<%i$P2J*w#;=@LKkiVDHRb2%>HP*LE4znZ2S*kB;E#(3Oz`hy(UVmupFJ(o4|9*E@ja*jKi{QtiaX){'
            'VerbHU6*s_rn8;R>(<Z1cMZ+P+dkK||_?g3v0ryEIq)AU*fe^G#5K9Z}Fu_L%sPH-'
            '57!FJZsl*tSZTIkE9X)w!<nZHa79tXv`i;f6Oz8|#K6|9fo7Dac$RIw`aKLy>iMI`6=XkzZEU3v)&LJ-'
            '#cMO`yHdV<nYtUkRzN$CN;lrR?1hew~?1YgN<cC990>0=HHO)2C343j_KF(ajgDgwF5(9X3N!ida$J~g;kOv7Gt>'
            '{Mc?>^N~EN(9ICG#ryl#Cq1Qaf`3GLLUL2)JW17pU8~JfM^-'
            '6ICoFx#3yW2YMAS29MX~GJH1{Dq*{6y;(5Jc!mr<VK0CdkaTl7Hn=-'
            'xt!Tjm>j+$Me8q&stVY!V_fNTPfigVRIKrKZljVEQS=IC4_2-p%_kJW)xl?#R7CGHI;F+-m%zpCZ@ae%%&rc+-'
            'A050ocyS1~EPrzN_}Pnt=lRj|gU5%*0bR>eS_n}NWp@>XgDNDhP`iiRK9x$Gu9Jh~$IqU@G4TSehf{;l434rEJfc'
            '@yUpx7x#@oXNz2>{9?X?@?mj}$+^giSisGr`o7%vgyU2Yn}&I$U;tP7BN7#VkgZURuwFEC@Kd(;X)d(w4*APi$fY'
            'y6kM)seG9MIKdiOXIBvk%=FL?+)BQ@!Q_`#vbx^E<`Ex_#CrSE!LGXlJL<G_&?*7V77OW>PyDkW4o!?9H56}s^PL'
            'UMb1oru5S+Zug;w+R<m+SnFTqnUR!8z2q9@If6HbwB@F$`Uw+wpkX&AllIMF5;eY?~7mboM_iWD@7uk{9fflM)Yc'
            '8@T%2W}b^LF&;6#hp@9hCA{=7`U{I&3(^UVDAArogT9gOu*41n+%<H_cBTT<IQv-'
            '*dmGe!@F3TF0#H^(o&A98v614KPX`WL9%%M<T165MK_$m)`wVWLD8x@*O=mox@vfaw^9#(T0DQ_Q7dgtfm2!xtuJ'
            'Qh%>9nl}-'
            'T?LK(If`}!O)n>c(sgcCZ@5Iz^*j=<0_iw*aJ7ffcWi%CP;Bl;mlH|i#Bb9Inw4Z8b~@VjRupc%vh7)LrS4a`jL+'
            'fBI4fg0B+bzpEpR+roDQr`=JTYFqiN(#wD4+RaxcHSj+l6*Gp*Bp1w*Q#9El@yIr!$zZINJ&0Mw6u)Dfey9!BN@v'
            'dx|_t=ao(ZGiIANN4x0XcaGG`BQbWJUi;&*4wx5!`g-'
            '%=g97<QpZq@n}!)F`a58=b9DGpfFo?D7*+mx4^1#8jWyV49L)o#DHB*jl=$#QeHD5uG>8u0~me}Y6`vtsOdT>}o`'
            'mZac9@023{f?%{G1_v5x2lNzRdnBhJ<ZG-'
            '#f#Q>aj4D(~o{HS<$Q(R$I%eStZklyabn=>Coo_D5%!%tAW`MCNt?HnfJq6i!T~xE5fDuhcSs!z|spjdVy}ZidS8'
            '5H}Cn+gy8shyfVsc@RGX09;e%iJu>z|B1&|@Oxsp0yl3$!{UwEZbilCq$(28M_YG{sulqK%QQJ0+URx6p6`)$@@b'
            's1Ogl%!TT13T^7I4Jl9sC&Lq30<)OO9zJ*ED|b51!S8s|NG$|vK+$9)<cRwWFs+ARPEO5`Fp+3gL;QWz4?*@py@t'
            'J15!<LCEEPoi+%auHOec}tH{@f5BK8=bs={fIF*{0Y5J<yCGK6e{Qx}c69=_UYB;JcWR=Kw9#&@NS!gsi(@xXq}='
            '%XhZni^E2t;Wm!&Rby&ucb40nAl-zWiAzR-'
            'D+YR8ggoP9B*dt0q|#zXqC3%&cXvL+>I|(iuX1eI*qe#t+?n<HHQpG0(+d1izLBc7Wukf?31SW!LH$caMl<<d^57'
            'EHq%uADxUL{CA?R_tqi41D!8IODIjRpWW<YvpN=sr6RhPeU7#cUdTRKF<Daf;ICo91F3<`kjpmZ-'
            'B1@ZyD=IduWNAx>BLrHxMi<s1%!q52<!9G2CxsSN6ys>dhPufz{fAXdXo)DdnvN@PX56_>xJME^l|e2g0DSQrKaW'
            'H8+Cn~Qz>f|6;)RaR&vc(vwcsQ)25vw@8<`AO!y84a3d$+ob}Z_2)Do;=B`Y<76D!{+mMs0cxr;(=8Mv$O9yXS0P'
            'IU4y46lf8yk|pRU~d7_PnXjy0?r5)V`SR?9FgHEOrfe3&5~C?zrb^CHkVwjNIH=Tp~5gkqeD@#(#WrT(`}y7TPVg'
            '|sc%Oj*irG0mTp8~pd2~)o{z+TrzdI;dU(_uppnv^P^cY^m6-t%%CX#!g|PfjH0}-4r-'
            'v_)Lv#kbpQOd*3{I`7Qv739V0sP;I3w=98GpE3q(&Z=Vfvy*v0!r<9_^}LQ8hU9=^EFVzs~f^68;{+3L`A40Uo`B'
            '<5sMMk^J~_vU(>jLM%*yn~?Fq?hQ*bx@!YCuSdmip!&w?nRx;o52SsTJ1CC#BGV>ivg?N2lYAmU@HAb5+;xpt6d9'
            '0yHLl-Z0&e1)E8<;vSrPhR+n*!3JA%a^@IQ8~_x7)I5ErBksH_@vGfr;Q3E!F*l{E)4uSbluA^WOe7hJG`Kf2}H-'
            'BT42?`_Opy8T!Bvi6-@2;Sr;HAj_uf@*gl3mD=-'
            '^nv}o1Y&XIM`|+<z|&3Z_b76k&N<{V)9%nKJY$ScZM=jaw77Iy`Lhar<5Y5QAd0}8c;u)-'
            '@eOczUY=uCZ^d#5#}@L2WWSc{<iF}OOQtjYyaM;zx(CY3hY7Ch70X}82cp$0`ct_E8BQpg0F^U8hd1*hmRuZvC!H'
            'ms<aQuEg|wpT+04|go(_5@#1VMsABN+yZm(hAzgPlMkWHYY*&jMdvaqnA$C&QZbL+qBA?_+No<LS}P<QH0#jL?hD'
            'p24|yha9^><>*6QB?4tuTV?HIH?@$#Fh>Ekd54eAgT=^o&xh5`s_S1_<CB1GqUlBa-vv>)fTYm@($>3>|>HfprJQ'
            '?yv%HbIvXIAFIRy0>M4^OYd*&|57OW)npG*=@@>;>KE7>j3S$p&V=1fz0w%j4VoiH<`)Q%243ZYuR>h<nXrcFLlo'
            '-Cl0GLTbKI(BkI*Mw+IwS0Q8QQ3GD*|!m=DzpsE7I0j5G$XJ4sbQ{oFql^#KJ(%KLy2o4bN~RgzvtFwAaXo{J#Gw'
            '#(oG=Gii`TCe^sGJ5aLt0L>AIsK{bJ>co<};`kcVqGn(@&McT!EhRPqM|4T9z1NXmfI&2|R7}UACzHAiKXERNA;O'
            '6bcscK;YZs7HL_)%O)P29bo21;B@vYtaREY+IKtdgF;4Jw*dEi?s`cM>~s))04i3_7fGTU%uM`2jN(#WU`^+#f#7'
            '>K_{u8rUE8wXzZk_Wfrwp<T>$g@INxjSCE!2d6Vc7F+9F{N^2vWxW!xnb#q%Uloo7%63yKyUPd7Nh;t6r9vRw%Ng'
            '30wnfg^1cLwB)49DGo<><r^;fyqCsEvvblh1H&qFYv9iu2FALzilk-i{GytxqWR4e+lzb=3$--'
            'Npzzs1usipC6f%!&ll6ARQ<o)lup_bGu0h&=NaPK9WN27m@4C0`;CAG3!%Y>*~>Lmr#xAIQ$cHX)RdaGA+dTKI`?'
            ')5Q8^Y48i?A*AbM&HQ&{M45Yr8mS0_DAG<6T56T=GO2sp~}fcXGZ(8VmjFXYGRC2csOm7)cA{w0r42!>8B+|{C6d'
            '0@h@xu|J<wV-EGo=SzXNMjmd|2HsCG{jRO<5w~(BHj%4(%+ba1W<^)8Kfs0Y&C|>CW8tSFEtP)vRY)QFy-'
            ';DixJ~qlEG*+yKY40$9L*7OHHt_sM+r&dxG<5!UZ5@V$$Qu`mrocW-mMbhh2EY290wSU{cf6gsgrF43<AiQ=jM^C'
            '^nj$9;WPHgS%g%HGN0Te)V!S4;S7`HXB}}rOtU$UGK||8u3BPEIImgRk&<e(*pwDMjS3AuWiZxQdL3==KVaXTglU'
            'SqFE3~dyZe=kJCRN5}sim9NX_WCd&viB)9GIS5z}on=S4*AM1^X3o1zFO|&*~}pion`wj$xJ@96fWZex_FZ9BuMy'
            '!eg-vstD-xVp5$`pf&WM&{Bq%GoI2A!2fTmW-'
            '|93vnf(uwcD4=li;y`HtwwVgF5&A(6a+4#T6%C<5_{U8Pf|Xu=4TBm<<9BMQD4aPwQ2Aj*+{V*bp^wO*c;H`*JM$'
            'qy}_4#<3vLHkbsb8qc?icjH^ZfS9>h=NU=l<RZJeckmiaWSJ`}S$VrPZG;D0%Z&&}I^=;;gLqp?5DNt3U|*{Wdmr'
            '6l7ud88O_amdGQ<w&W<&S()e=b%hi-G$Fd+ZSdNo;HyB7=5Z-'
            '){J*!UTX+Yp@hG2Lxkz*v$2A{dG|P`JSi7c{Mx*W-'
            'i|DilKFOqwOK&x+xet9rJXf+RpusGCY=DgkkzxtIWbgiXNs0@$RY)&xUhtYYH*d*gadMo=c`Mmgo&#<}Vvopd_0l'
            '5B}$evXpx%)i@@tiOkUptqzb-iD{x(mzn;kLruynwoyuxD?Yzi<!trsLq)X!)K~f4_6*(+G{^dV^_Zyx%Ud`Y-'
            '27mpPEnjRM+0roikVG8FOgz8)I&aWP;m<+jQS%MGO4P-'
            'xjVVo;7Rx+RlZ(OTL+FTPv6J{&s|E{_(GMeVMN@SHhZAa_DX*@_>dD;ke0Z$V0mZUJ%&6Xc`<NkBwT!6W-vDKs*-'
            'ONAfwKjKRza)|3;+xJbN%G1fB!<Y&kbSLc?$PE3AqWeZd8=#NHX1YZs6mW}NrSj%VHHJY*yl0(owXIh+I`9ZeLon'
            'tzZo6Z%f!1SlZCGI&59vbH0Lmvzg@gustsJV-o$xU4w$LZW!Zq)PKW%}*mvTf*##8#cH72)Ix05`@$ZrNLk-'
            'sKf=1DHX;<6sSX<W@wMTlKN4hhq-IFyx(MN@-i{e@lE1dho<Wk-'
            'n0qC1hq{YUMaz8Wb<gzW8*`OK~2hhzRW0Ys6Y&4qj3_of#~^wS<=2o|37hZ#*H>7s<hs<NJp%P;hv-'
            '`|#W3CyFLW9*!RX5;qqmDg5vlaPfet$cO+gqq<HKWMeQH03jYsz!gE9n=$FEnUmcCPPT+$6<b2w25}(9SPuU!*mO'
            'V{ev7LKWsF{-P`D~qNe$v*!-;@_tAQ5AP)dLn4~y^*YStK6Q&ZS6B_6?D&C6A@W)WbARc+)VWGF^V+F*-'
            '%nK7rz0Hr3UStr6RPxB563Y-v%GmsD&F-DWhQ!H0K2TlTp696Fkf*xe!?Q-'
            'XNsjT?kJ4hFehYI0XZIBR`#W2W~nM@6vnNQJ4eaIcQO$8{{1E+%;Gh)2$H1(}}8(5C10dd6ZO<AtQT&b18KCGRz_'
            '#Rh5;4WS&)(kGNl-kX_*<4;uq?S{C-U}!~feO}ZjA|yeAr-ly$ap8*T`@5Un`zXTW0SpMU#m<)TYT}l1l69Z6Uhm'
            '&E&&ziz*WE7Jws~GEbOy3PYu>e?Q1W&QUAWZf8&Ac*3`$%vBIrfipi+LC<-'
            '7>4~w6b4q>=a?t}kwdg$GnebJLg{c@XH>enEa%usc@Xg(d5sMJ>IIJ-'
            '0FOif}IwKH_lySgYAmx^)6)is!Ni0U(G9vzdJl6k!q$IF&QW=7&}{!CG`(jKn;`_Qq^-V51&fC<J&l|xjer7E-'
            'S`O;Xv_i*>rvcEGPDuee!C&w-gF3m~vbUYp>!yBv54pvo9F6&j1rJ3vUrgPxYK$*_L)PB$OA_%-'
            'en_qfldnZmJC~eES_iPaNxb2!02G{Lh_H7rB0d?l>!n}KMK|K%Itu_*)L6O~r2vDzm9GfeD_N0;4e8X8v8O7ZVXz'
            'XZT2w`pO@=f>C@T$`%riUtf?Ebeuy)n?+y>Cu4iwLK`R-'
            'yw9t*l0FGLR)E0J~UUibvbewI}>{DQB!?8s1RfBlxC&&8yAjS+OE2Cbc1Y22J7kw=ne^*<nffM<$pt7D2T-'
            'Xg`?sf{CQcs`In1?GeaI^M;sR;vcV8Y>QVW@eAN(;kOO)KBTUuELH>$BlSnk>!z>t$G~%vN|XOloi)oxaL(c%Za&'
            'U=`rX<0H+WLxqM1&XGVsn0yvc6AyMOlmzWKIUeOhz<2q)wi{Ikq(A8e1@VL^9@N+ZhkZuotvBrgOG%6^DUp`G3x^'
            'Qmtdz>Ec_Df!~T**C?*-'
            'PCCyfhw8<M^P+jW;#)B4GVDRBEGR@va|pBVESO%d$MOQe?EBr?1`MNb?E>3hi|^w?Y|ExtxmcAOu4=`Jp)tm6f-'
            '*@#t=`x1!Y;g)luBap7$^@Px6=>0ng+2xs`EAGPe%k_IJ(tdQp52-_PpVb#ik9I8m*ENx3XR!hvU^YIYh-hy93uz'
            '|8o2$-j-iS*{-'
            '?1d+Yu3lM)FJpBEm<QAQRE*_{+xbXvO3rxv*S?wje@PA(~KP0=N`4U^pA0Mb6zPm3L_T9w;`@)#C051ysKKO3=J='
            '`lP4({RYNvuwRRG;L)#Me|@Rv3bG415#BD86F|dF6oU8{m0^Lkecf8m|!_jUhvQAJ>;>WyQK=v-'
            '?zkH%9pG{t`iv5ajk#2I>yTmU{^CM=8R{PeRrt!_8$ThgV<S(ZpHbn3v&J9;-'
            'PC?8BvT+$XyY9E`x;3{M>91C&%6HGb=^R^__Tqz<!`G6u9)L27vcO$OJ03s3(ko;Ev8f^_<rmuvEM04}E7!L8CeX'
            '4?W(2Kl4w<8oGfo2*zR8Hm|EFPfIbXX(K@L6s|~dXuS@mGV~jTA^b0w@ry!7fLn4`5|QiA2jZWb&OxH9|KFDl$Vr'
            'k_4S)#x_&xJULOMu!T(){di<~{We5GnzJ83jsr_+YQ-XivZ#?Gblk3`aW1^2Zm-UGhY37&N{1?PW^Bb0sd?Jj_%D'
            'IOU;!;bjX`s3h9rCM8a!V>=i${sToy?jY$}_w(ZQip^O?p1))>LW@bLW~!bPEE~jfMZWUdJ~Dm8in_kO$xFy1z<L'
            '3}5^I8q0q?n~k3rfNrbI(tX>byjr1)AqS!uU>_Ub$ImC#jA%i-'
            'u^@eIGWl3$Q)C;J`FYoMvXDc8bT}&%nl1Sp=_L4{w!U8cK0Ygelnr?Y?TeY)s}WhsodtnZV&^SSvtZh)N*xNas6W'
            'ErL%Ghe{x&|otn2l~QTgF=vOHPAyNq1mh*+-'
            '7b}2+wU3nBL?%j6drQ7Wnb<%xFpJ$wCRb1f#hAPzbF{m>aYo8%%))lAC3`>_6xf6y19j?k58Fo0$gjg(n96I55EF'
            '=}>`Ni68&tKgR{I<DmSNiTyK9t?@!-'
            'uv8W62tx&VIY!IN=aAzA51q`n?}~>jg`pqlScs0i2!W;dmGN@P2F<3fX7hrejVxFE>IQ{ZYx7R$<5vdDJh;Xi%q7'
            'q#mLgDBQrtmT(*LoF_yN|L#5Vv8lrEee24J7LT?nda1#TXYmW+uyw3<bKw6rD_9J7bMZzFhSWQYBKU{$a&zg8VBQ'
            'o$@NWX^%qgiT<|_(SD92pck@4?SK{9F(+(I{q^h(1p_{v(MLj(l9oxFF0*5yxYB(4i2l6+xC;^Kr`(-'
            'cE<zL7P1@Q7!t$<<>%*(MZ>@9-'
            'Up*C3`Se5X`e@ZLXIs1<G!1aAPT+p>d5Kmi2<&IW;QKRT4W9^?ngd_@HJo^#CiBuNc)RG45Dxl<%HN<u@yf_k_eV'
            '_7?LSvxj`Zrd~WKEsH86zRpeNpw<UkDN2G_7s9surfIFw<4Q_qMBnKD^kmxTt-'
            '4|qbWM2T0~CQQN35yH5ix8%gtgDEQU&1iMiO`zTot^NP{3-'
            'Sz8xz^TL(&4ET$&P=pvCP+EvL$aua$4iPQQ#<v~?&)GRbpK15>ABN%LdH0f`)lTp%Sf|?9q~v6PYCeozWNVn~p3}'
            '(}!I@7z6m1g*7TDcTjy&oCWl1xTPBOYN+{F#)6QE=;)<?hwuuwQuYQe01QaoG>UhU0KqNVH2F(Ri|wN$-'
            'FoLz_rnx~7&Isf$-{hL?OPXCSFa7omIc!_#7`(-'
            's*hU>(4a$vR^G1waQoG)uF{xi8kzgE$ACZY|>Mkt!oQ8#}dKEiM2-'
            '+uk=zol9Dor#}E+m#ixInHXTm!Z#Vu*DPGF-qWYNI-1Ci!78I=ZK?q%|nf7Hg^Kf%kwlSqLCI<Guh!(I-'
            'a+TJSa4hWtPgxtdnTfXf=Omt<oBl)lY1>Tsm7LTL7nniUUthm+2^3*(viymNVh+EAxg4HGQC*6^5sTts>I2XIMAP'
            '#*SG-wif0IHYA$X0W};ZADcZ=o^CN?gU-'
            '&{6uHW}JA{9|H}s;EOUH6trtLv1>NtK00ueH0Vx{yErAXD_K#WYO_6>c2QBiF_eTI0zez%KjjPNFpEDV~y_7sT}%'
            'fxz7<<&@Pv9amR$_p7!W;3<7VY;&;d!!>-'
            'Q*2)<X%Ai=Jpc3Yv*Y~b!HdKAAlmzOX9qp6cGmTdaL_Wao{KW>r^M;z>lG%^Hnwih{2#Agy}-'
            '1shyUy3@a4&|Zg^2Fmiy_vWEGd~4vVqw6jeUa8dm8hms%Am<<VjSkarb(Y>1ul;nPRlA)mfdiHYXMg<T=ZNuQlp^'
            '-8Id?=L1BEK6jhkCs+$Ve}N^*cNToSRo<~p8tla#*`s^D0I?$@Q{hS>}b8IN+bGMqPCpXZ<L&mk&9iTg<jjNl?zu'
            'tm#x_`dR36wm-NcCFUF?jV#BJRp_PVGj>$h0fwJRr{ojKOHP1a+U{;rF6^<x!3qFDaovfx8?DdF1o>b>{3>cpXQ1'
            '$EeMU6$3i|J-'
            '9yt10>W~@KxqOh_DYyIKwzT*nAYRzy#W(BR;?euz$HB8p1a1@Y1`y&0LrKvHtaRy`gGm?;D=Jh`?!zXUkIS1w`s`'
            'urprYA5F!sX1E)A*UrT{gK@<ef1g7s=w#Wsyoqw#JJHr~Qw~lSX;Pg-spZu+fdXF>}geN#mAi6JY`hhW(=6dx7aD'
            'L^aH&R)(Licb+f_SrwO5s;<=3R~vuYOfp?27-rByjeaR-'
            'z`ZvCTg|~4Y#A2uY+YRbY!&1+F~RuCrJ;=vSUB1H_~W1I51xtVIa=h6zhCe(3QbKD&#FELRB5~+k2cN4pEm2YwVD'
            '&WW4ycYSKOEJ%g@fbl!d}{|DYrY7=fHS-'
            '(?yQ8KOObgC^9HmcnNem4^aOndv70)HcTq$ay{l?3+6zRnfW4lB!s%wsx5Tkt1h5Ru{?&FtwZDy}xE%c(e&2AlDc'
            'd#er0%tTfP`+|1Ysn0mGhO--fK`2~kfMcj&QUMDtIt21cl5X?-'
            'fyu+N5)?z0OuItpxpCl7Tk{p!>vRK%ej?}y$J^cbKdwnIXh0H{;r-'
            'L#vE6hp$&;R~^wEb{w+7GQ^;q+0j^5DVl?kM?I8WF=Yzo=)xi>|LxY_Y$LVMp}uaQB1tdR3ln)&=*(3#C4de>upX'
            '6zJLis(Orxxuq@48fih74fQqp>M`~^$*BPLo2g8T!=xe*7RoWlRK@HH1qVWK_CVCRRt)b9Rh<9`u)x<qXsE^Fakv'
            'MC^&QLj2N<RJfYh*DQ_<>kU;<at<QN$60))v03Y6$6SzkR$o&qyTRqr{y5k_lRyrpDC#BC{N<Iu3QDAP-nTQ{C3t'
            'dVb6L^6ejduc}4BcCK$Gr&T4I5)V8S0V)10Iz&9ftL(!UeP7W3q=}-D?+-'
            '2^0znRww!||A`k)#&B@TVvue~rF@Z62X!do`P#MUk^<s00jO9aMm05JQNPOn!?qv^e)zKa5o~Vdx6B~a*=Sz&nIk'
            'S1+{C;Z@0AW6RLnCR`DEWP4uUTX;vNVFM@mH*>yZDie0dyk+#*(+J+Ca}<$!@{FzjCG;8IKD5TjOwg+JX%Biug9d'
            ';r>bF3JYkMTy|#cbrN6R)K|^+Go#Xat653QeGD(~qEO#@PkT5k*C$+^y&3wG7(W9UHygL^rKXI&BFKLzqJO-'
            '+fIziITJ$&k7TiQ=;e7U10fDaM`+JF1{h~)cd-'
            '<PRzZy}oSTw=6Tgs3@wOdSouG;$!gOM&@4Q)tJNf?gW)vml*s;eeg<r2ij3=a(ido3Nk(nyoz>7=TV<Fi6=#^aE>'
            '_cT~#j>*i3D@9soPp}OfJ<)Bh`R=mbLtRNF)Prp8z=55V%a)cl0@JXBo^qvB$ZZhAd1jOzQ`_dGR%YMmB@rn%9>Z'
            '=Qv*<sb)>VZT3BgFpo16>PK*zhJ$97hU>giQY_-aT@p_P$tuHFDvkpx7pR7xHirbpuE5TjUOxtVacm+(`l3o1l%l'
            '~^*|*J6-Dg8-8g=_;9_P%lF7e6m<X`aZ_rlY_+~%oCG#y`v{w-'
            'lHc^qx&{q+?JgiFIZq8D+fl)nhajfUlMUkvCZIb<RbQlxvjJtX~t7vVBdMzEL*jsPNZ|?UD_xDMMkiiwxUsF0BnG'
            'Kdk<uajG&rzp;TA@9D}>iMY=a`c_R*j#LtG3F-'
            '#XP5kthj^J3Bm=wu8dx7e09+(6tg$f!kMyfNMgU)cDm!ah`=K*>(TG>=fgs!UnUsw)|m+rlzr$@#M!p{`YoaZ$H*'
            '4^Lf7gLr`!#-'
            '1LrAf>W#@U9c){d=v(KL6GQF{xxb5V1caVkbB<>*Wv060_=x#f}KBQ>g$Y_wuf#MD9ZCnw}UZr}7d2Qq3rJEoOWm'
            'hKH3a23=(i=utQ$6xs&JnnS*@4Hr5T0&({?qL-'
            '_6BZqXQ1ax%(yO%^qL|CqC0yzR1U>n@WrfTZNdzRZpH0Tb6t1IxZtlqq%oEWVeLk>_pIc2CKOz2@5g<Bb~N2EpQx'
            '<{JoyA)~Q()vg<>!8|}<)LS!aSRFk<|bKm4E5ovs>m7|Y$W&02C-(x>s5i(FCWC%QNdoyJ|UJ_M6YWVTo!G!t#-'
            '!j8=4x+^{o(?p|JX4oWDO?)YEsz<#`2?Y+xOh@E|1r;cnJzG$S=eK(C&!cqCiH4^R=B=AqYdgp`^CnUXGd1|tVs*'
            'i2yQwBN$OsIq1+2{n?VTVol`*lnp~si4-%?=GFAhrVluo;1=;P{i=kqV5{*Fn^j%-(fk_YNj2MrvFxaJN<*}kVG-'
            '7F~5#J!_Mc^+3cY|?Dpf#|1kZ18dtZOBB~*w_Ba!6!gZ8Y>Ipbd7b{!umNG`gibrYXthBZ4cbB!YU}hL|eZr`+$@'
            'o5gq-`2?J;aW62v(>59W8Do5}j|CN8!%eF_m&g&nL1SU>-2)7AwQJ-'
            '3|8i#S!0QPN3Zc2utv~qpcv6Y$NTb+ljhL>Y8hYC4xhg&X6aXqhpesm@;#fv1I!m121@=akzQ=!b8`%p#OwCS2;S'
            '~(<=gMm`K$F%srCO?O~=69IhwmqX{3k2SAvP#c86qz39172&J7t@z%tMFevVFu$>q=7YR=Ma)oa4&D&3fSmEcZ@B'
            '7ek<B?ox*DlTs)S5)a_BykYPZ{?28{OA6Ps^0WXrkQ@C{~dH^Im_m)AyE3Y3oyGbjv~&BK139zlY8+%$ym65tA0-'
            'ykw{~>}_)?V(YE!(g<?-xpEja*V@Va2@e%0^5Kn*av*<xyL+nmnxG;-'
            'wuH7=A(>=_>%$lTIrU2@Q^u8%mtw`Z(;;Ke?f#8r?YT{R+I!k1kuZIM%Y0E^p*ciUOES^S_MqmM8^|j!uetrT3i)'
            '9_<^jl4V2`RV1$<~?ePub^8-'
            'YT%_pP}fNqo3Ze*Ty^O?(IrcrS^#(s!obiyB!RMrssoZJL+2p@Q=;!`2q`r2REL<p>rEcwdODQ$>a0E>-'
            '0zIJ&|<gSv7wzX}tnMVgY`4n29KBOqJyoe4IVL)RjuFE-kgO^T2%nV+Kb=-'
            'Lt~t)$oL?CSHJGjIx$5J;k}1W)|Mi&A%-'
            '%a|dC?d{5cejllt<xuAyZfm%t?v(a6UK!qLVWuQFhWyW_Vt?TL3<U}P%Y0;U^!PREmUe8<0mCsD-'
            'B%{nw1@?B#jjP*vYFP*+WB&PHCds_xP4PTBKm4$m0EzImdH!x7HLmA20Afyyh<xB<3@zhRh5sC{#|M7pz~C%M(9S'
            '3gmv=F_kOLyRjIqrK(kDJfz(`;AlEp77LD2#D!SE@yY}V)II_EN{nCDWi(XmzpIl@B54nA|1lUDxK-'
            '`6Ni|1wwkJV1k)sSDQ%PRjQ03Ahq_^%0OLsb+;B_**a5HqJDTxy@497PQdmM_<}QVR_uD<U`fk?-'
            'g}QpNvVrY;P}UMY+%WGq#Vf5&|u$+UW>R9ORh+tug5Q^A@mEBW%!BC$!>1bi1CXTjVW+Dy}PPeybN1$blg89HE6&'
            '9o_H#q;Gq%7Z&lm^nEo_-UYSB)_{S3}hk$H)C20b(yEUn*AFKDc^o+t@X>(-'
            '>q(Y>sbUP@m}^VUNL<(W?2+v>6N>0A$Z|~BD&CWP%4VYh3bvya+_xTnH?`Ov%`7cH8eP0NFjTJE7FdVTz+C@f&5x'
            '8W@aP&(`eAo7@=8MODwmSElFcr2*g&J1HqO@py*nDu=P&zz+Dw`@Sk)=9>2fE`tJGbvn-'
            '{p(Id`DU|NpdQEcT|>pTY6+YOtJiK2FdUbeqGsnYq0i!0Q7=)p}cxvV(tE9Ng5Y{wyMEw?Aard>Vy>ctI?IZ}*PY'
            's3>`uqjki6)fazV73E9pHvY{-'
            'NJy~u0ZPN1HYrowF0tZ$rt*RNs|A;<O`O}VrBP6dpiaE`6<5d4B}5A1%I5N+fT^dO2EzjC0Be_xx$;cqh#CmM;^E'
            '2>Pr>=%~m~GW9oz4?~P6|&OCeo9f*)~G2i|O7)8F0iCR}}W17c36GMqv@p9qcgMuC#h3HQ#xkh?P_loB=aof#Z&-'
            '{*OvIV!_TUXWc1ZXK?;RMmOzQer?vT>DBFIpazQG+%W-'
            '%e`mWoKKXX<u)W9x|wsJspu#JcjKH51C8E^GTuXo!fep$O5jRp(yn7Dc%mIl-'
            '5Nt`bvsA!9?H2<+*(n99BrtT!54-'
            'AtkC3(*BKo+sCZHaSJBhhO3P#j$G<C+BonaH_%6M;=9Xz<h5j})3|M@>9N9VQwp;l(wLt3p`19oMV!^9GMaOYd}J'
            '`?v)(Z(3q6?iW0Yti2-'
            'sJVyjW*Cz@RR46TmN&M`O^B6p?R163s52a2oUgArZN2yhN|aTccIgO0YlX1p9&MF$)uRX_DbrV~kTsN8M=zEy(Qk'
            'p=g*SUetTUl<-4qglt@VSi+6KVobw~vqE~gK+&H@3^Hyu^LhDUJOv(bUN2_D467ffxcoHWwV<a~1JLpFC`0a-'
            'bt07P>>^b>AmSeixeU^}4SM;`%>P2LPl{j$fEkmbh!$?m^i}rZiVIyh_czwhc$N1oRZXBSUkD|<W}j6z<LU>xv;('
            'bW>x{y0mbpJP&^@d$^=oA(Vn915X=BinVGEuzkO6mAt_oT2m7EkbT%8669(L;)?5^X>ckpjaE`Ua!eUjw3%tc<m+'
            'Yk8A|J_)B5v62$v{9N&wUsm;2F?u2U5|qjG-'
            '60Ndxq`@>e}oH#+gb8NY`S<o?Ax&s&YumTsDC+Di{NQ>VO@81cJclM+w)V)o!3sJ_j_}tWeNQQ-'
            '}HI^h^|xYNcu#hVzx60Rx@ZcwqXgE9NN@uAV+d$#N0+C6Fc;ubxLlvQdwxGz;$6P2-'
            'b#?<~i4rCr@ya`6~{#z%QkR+!WM$!5jmZr6AB6lW+(Pz((m8wm(!w%fW7sGxFDEdwYNpG7enM)Coi!Bu+~_U9J~?'
            ')7zeYpn1zU~|)(r<kO;EAd=moRC4i<f?vrT^bo_cw>Umb{6#Eb(<m1_Q|Yl?1qZ@49#gif%zS61Gyy|1H4xteQwU'
            'eKwG76|MOtyKPEeW-QD@aINv$FhfbY&DsjaYwEZoLdQmBK6{XpQMkVrY2<FLspzbHJGvz~c&vI|~_p@7bqp^d$@g'
            'Z_+@G;|Mb>8RTqCR6=YTf@yUCi#TiT{M!`1a-9K`Vb}&3s>PuWrr#8OR(f_Vz*!t<%#>cm*+m3#k3K1l-'
            '5k1o|UmyKSJ$KG1F>xU-$0myKszd%>M-'
            '1|MTLxPzrCXg{FCyn~V8Z)y+RLS23*wRzfOn7hXzDgDv<qQ;k5{B0>|^JSYe?q>kB{W$kMj4i#6J;|c&ypF>B+vw'
            'vCYGnJxN`Z(?3~j?n7h{Kb8}7nepa8!cHaM~^nCPG!cW>WGL)h^`%|#vxZLjfo<-'
            'nbZ@mLmI;7PKu94%xTyKd87BD5B9gH_1oe|*6=j#ae5ea>eRZA7k``|U4{@b%jtc0AR`t^-'
            'fZbk+6dw^J|iW6R6m=hp9c5dc<%=+esj=BYCWlJ+GXZfzw|2ePMp>B~@Ip{!S#8aWna=lH~FCQKFVC(Aft59-'
            '3vCMzLj`ehARnZqlxzP9v(!xpOTDveyNk>>GcVg@mRt7UZl&U(-'
            'S?gID`e=|^ri%D{*X_H(PD^1)V5o=AWakYIhM>$l$3OGe>6?wP?0T~Zp1A4HTqUb)~EEd=L@xg_&$%GTbCuN22iU'
            'X-'
            '$Wb;#KOFg|7FEl}nir#P=>pE23Xd|M+M6zsz2zcR)NU9#`<)(>ALn(#*VG`x{SQ@>Qd7pMnppJ36G_n?rRCo7rM3'
            'QCcVk4LBu2-'
            'S2+h0e8?wA29uIjeUe4W*)nwH|9Z6Ts&q0arZ#crAY!}=2W1_eyx7;_~OydvV|V_B4|@9n><;bB@|E*Av>CG1f2S'
            'lmKVY?`N<-'
            '8%cCYdLJP7`qG`j3`GvmA}v^G+E@5&e4#JaFEDKK+_~X1fuXr_dboWuG>)8ZszXG+H@Qjp&xo03!=>R-'
            'FUc1Sds`9Q%)9Ur7Z$@D=pM>cHmfVi)+L`!QxqIf#L}WV7Fe>sMS5n_Sy)U$3-'
            'agXRwlcCRQI3cQU#<{t4YBLA_r*{Bzf847s<3s{11izjx3YY!#>69;58jZGnaTjKE!n;JCmaqRam@M%)My`hjEZ;'
            '5bH{5QY9_8+t>9<br0hZ4h1|y|DyNK`K_!f7<L5*qEan&PN)So$@f0I^-'
            'Y0wv1#FxRez}9GXQYKAXjO8|$xu5v~)mo9E@u=2}mbzmt_#hN{k#hgBs1hoTqtRjhugh@2++8@opOoro~&Zul{i?'
            '><~-'
            'WX8QgT!ExEZKbaaYZRKMSgiw@kOoohof*2#{bB@1okHAHE9P%`KYQrbg63{z*cLcS2JNsly7OWFbk>FK4a|44HuS'
            'YRbX$G5(}-_rzYS~36;VN5ciLlsE%o93HhzbsFI$>nJadfNc-V}xzF5_p^NU^}krow-'
            '%=lh7PbE}q9C`msc+tD8EB$bzzqO_PA&RSz?+95Rs)}V1bO{fY)ozb^Cb>yNa8!wNK-jI{MRl6(pxh3OaS-'
            ';l>}+e@aV$Liq_h(iw)OCv(b`ZNe8m5@H{Q~ulJyWIK8bxKsN3ji6#3`2iJ0t3m^BG2c>iTf`Ijx_6WCH1Qh!%73'
            'fW5{C-'
            'g5f%0I6e<<4f1|KE}>#Y6R@Uy(bZ0rI)%*VYE0zY)pubfgNPJuO=|`k?M^wb}+f`=jQ^p=C(<A4SKzzM}2uwgsvQ'
            'G;24RwHd8G%5d1<S}65#B8Z;TH*IMbv{3GEYlkDH^FOp1PG>swjBc?h9UGgd=bYD~6m+f<dbg$pQ*jZp9`s)SWEe'
            '(id(TmMi+GEuzU*JAkN!DQAH{8XDzE}+saQlLw1SZdjRI{hzBrD=a5G~?zW|GmwsUsv_m_h=FQ2{qVb4&#i6qM{0'
            'BGB<2b>@PI#LGr2o`pe*-C1ns{+W(v^gNfozvQWj!d?FGN?EyZnJHCu+uk^%qh6D#3;78qpR7-'
            'Z4wU?VOsT>+1Xu%K_?m?cbCkrcNRQkO0xhy3(U~K@VBqg(RrgtQAGzSd_W5P_g-'
            '>PUAJYCX?xn7E#i3N$rN`ey@W+#S2ESgNA_9OEQ!0qMgz`6Lv{biF9J&em9j-'
            'MG(wg_OHEUWA#C90n!gCbdX=bQB$=C%L_yZ@q(bT^uE-dM;q|H|%*fV{W;k>_(8zgSz@ek$s@FA2@@FrPj}9N7yn'
            '2(rIsD<-'
            '@yVM%=LaVzZ=U_>r<21`^7fPg#sAIW$2<+i7&}wyGw_IoZ0ac;dtz4$W(mmY<rre31fz*sBrF(@s7ols!8RB56%q'
            'n?q#OS*F=`9<968y4M|Kx!u0F`gqNF0LO4+{zJcI>fy%F<KPwF!y5BgwN#W^%1`G^kmj^~(JgGuc??}C48?l7<%P'
            'h1-2C`kz8k%wR9lhyg=5@8#=u)+z;L)ec+TAP#sXUR)K%oS7ag-RQZc>@+`G+o(#Ibv7|A<hCcgR8%)uZ_~l7T7Y'
            'gEn?!(`m&moKy>VH#3cZ!XI~J7$EbA}!V$dROOA`*HU)5tZ(-_FyM~B!D(cAKXQY}infgS7@yx%i(L--tUg9t;cm'
            'T15w`Kz!eluVsR+`f-'
            '&Y_!8n`)>>5v}4RRW}_QqYKD>A>P;es%lKWNxZj2W%2XZJ5QK_f>q9vvuiFpr)C)sSOdUye32dC;pH&<{E^{Z9Pw'
            '9%notQM(54qPZbE(<D&9uHaV&pRmk)P~ot0`)d!rtUUkAz%*02Kra#fnyYQzbn=*As*aMV$fU&a*>+1xJK)JQ3vT'
            '6(M(_NpdJz`=EZtJC|Up~Oi5O3%x4RDdZLHWK{Bn#R@U@~l|BnjgvWo(VZdECMTrxkLOeQgkN3f$2x$=z4uoR}7~'
            'HX)7#uwwZc)1YLE7R8)+Ts|(C;%!tK2RFmAei@O~=<H5^L7>4M^MZ6V5E{f_@_Um9UVVOiXYhUy970~PO<3{hYLc'
            'SYIGYt&hp0T+2M(H~r;w|He=Fm`OlNx-0^|}k9stABumV5yQ9-'
            'BTIgxG#N&r~p;JXA5%uYq9?r0$!;%#Q+Zg!AZ!$&Gyavq6Y|Y2ktT3P*7{DDz?2DeJVzIiomq+8H#tlPIG$h>N&3'
            'SHu=GOmbcWek&RskP<@rLPex3mlZY}D#a89X6ofem5B7H!mA0?Cnw67=cs8;^BmvMJQwNW=t0c}{~xAOF*^'
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
