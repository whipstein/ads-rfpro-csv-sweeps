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
        'bb549d085d05f50cb2205992597bcc34f7446772980ab09b91dccb1cf6ac424a',
        (
            'c-rl~>2@3El_>fjPf;n~b&Rq=n3Ch14rL~nktmz1HBcgLpR~-'
            'bfIxw)7FY$N08tE^Yn_L<&u|~?Jjva|HxE?>O3H9o(!CO~@QwT1-'
            '~RTz(=<J**2QWvU6=2R#Z9tY74OU9I=Lw7t75&nNhZ}SX(sQBS@NQ2F26pmSL-Heu8U%stcqr{fWOKrdGqXeRgVX'
            'QH=8P1UzX5fx+<4z_^Byp1$-)!dRd5eFiHJi#dJMRj@C)>VF^<-'
            ')TAjE@VS@`Ce>td)0EAZO;Sy8WyxRuvYf0Yu%u#jQvA9ps%g>u<u9XTvRp38qDktiNS1Y3t&<7-'
            'f3hyGVAdK(9q``dq$AqVs+hy-FQFr?2<A~6#_f-jXZ0#+>ILq5T354jUDg%sbUm0(s${Zg>SR$*W;7P;0Dz(f@_@'
            'x)663zClcv1dEG9JIV6rNb>8hB(rbh{EYlHtg12E7BSVIjvSY4M*kzCcYa$XiQfbuDVb5&lH04BMw9R;6cUaxS5C'
            'c)8R_I1626<uEz6+s!!WC<PW)nK})o1z&fIG#8#n7cd&d{`qg%xVBoRj+AJ)K{L|AWhT3V7{ual02Vp)|*w4=Sg`'
            '*keF1^M{IB)zpXA{flVR*zFc1|<iAT;^t!GWjr?#mSzpS3*Xrv^b#6B2un@oi^;>hJ{)tD=E1ON$lPSOf_9&O8K5'
            '>gBOa%LtzaHbf^uzjQSymVF`$2Ux0$c^KoG*$|@&b?!ejOze69<FA7s(+Y3FAINTA~Bqh!ckGw7$ARgqae6VDbi!'
            '=wfqKRO@CuczXEk;K%2u`N7MB=YKvqI>}!iyf{qu6M(e*=|5h*dXb;L$`Ak7>EX-'
            'M6Zr8N;9>!@zua8Gu_g69nE_q^)=lP!3V3F-'
            'Vp?7yqR{mK<VcR6J~Qxrve*=Ki8ohz5pNEUU%ffaj}P9!B2EwA<WCQu9KASro*zFycyfp{e>2FBUY;BuJ~@5$2AY'
            '3=baMLU&-'
            'uaW>6@cJ{dh_X&sTFer<|xoE+@<t{x#_!e{p#7L;l0T%csu|+XuOV3zg5xX1SQ$<d*=(MFIT>ga2C{=@3rtuSK<g'
            'y4n=kfIcNBIQ37s!@WTQ{{ggp1(c$|P2;7L<b??ufr9QdLU7X*tDX5|iiof(fG{?2PK4HD!hRf2UAnx2|J_TP^@_'
            'gJNPCDl^ru)i|K4lO$9P!wnu$=tlJ!LgggP%PT2ex2i&RkVNZ_WiRvZ$bKPx`$!EvwYqip7WH-'
            '>h9VuaaC)|=&`c&i~iO2*^yS?Bg%ui;AICDpq-'
            'N1D<Q;AiFJqN<y9Ic<`61zeiR0(XO0i?|HSS|V{24+*>}E9XS$L737<4gcj0K12DuT)?5wEvK)G4UkadYx3VfpR2'
            '+hC%>LFxuDW}$vIFeYEe}0%T-'
            '<B?WGoy(uyWsaQI%_hc^Y%nB&QXjiQ8+JA7wX)C3OxLStvW#HGQt=I00Sf<XdT{lY!;Jp-'
            'rY5td?|=APk>HMkCi#xz)tRMH2~bh0F}U#wR3in=hZBCLXYvT5?g<h)oIKXriwA5D5Q-_Vn3!-Jkx-lKR?B`Dx_P'
            '3!l?%6@inCJhJu=;pX{xk2M|y;(0eYXfKGHB+e0{|#M7*#Au6y8zr}{toU5Z`KCsWdy@E)#Ux8T;Q7mxHD-GVYdg'
            '>QS}}WuwLCLXq`;vz%B3_m7EuAIQj~in0a}zK^QTuBgAM7_Ra)tW85dfih1x6E%Wo6Tp*bVCHOFM&(nff*)*`eTo'
            'I*ms%Z*!_L>qXd$iwFz&}hci&@S~gacPC>F`ubgV^{DxJ5A+8_j_P@$5rjQ|BX(oMy?+AKV>_<L0Bm{~#TM=YLkh'
            ';R>2NlIRRCFpfO-'
            '0IPb_m7Kc+B>Vf;VyxzTQgBf#G0njFO6aKeYGNd<f;LNA>v_6+?gZ3hXf0}JELUznvsxgW0*#_DazVtukJar<N@i'
            'qnw?Y8W4e;Wc4b)&+|7-Y^U-'
            '%!0G4Wou^(9CpSDOad+0B|BG|3){*V+;nV8^RsrLQ1L4!OLC`T{ar1&fBOfSeKD6XW&4<AhUOPvD6QFi*qaYdNB?'
            '++r`XyU~E~K_fOS^xu)BOyq9l767G|_|Iy3Bi?a5P5!h7`2x6Arr(oAeWCZuiw2UkpDfB|t#Ri9eps(pLu1vWq=S'
            'VVC2!9dxA?ySIq;k()y+`dBRqWGvwcAk-Q;323$f|b7}f!M8FE*Rz|FmusV35Aw}4ln__T*7C{pMQ-'
            '|&2JjG^<ZD>yI~D)^<?R44&Abb`1<eSQF90Zo9bP5+oCeEw5527jvtR_7Wf$L47dLgZG`2;LkuIU9V!0|!oy)F1h'
            ';>l{vOjdFa>OzM!13m&IE31N_U$Fk8F_$@f-'
            '>vDZLOc!Of`H*HF9flvyfBi5$A2)Rx8U&w_^t!CRd6fEne}x}r^>s6zEf(?Kv&jnDrQxZk^|YRhXE*R~9$_^>wT2'
            'J|4v~u-&eI>OX0sFw?Q39p#qfK{tvTCWs(`krr}z>EK;|+11Vj9XLivN{9nM0p4RuOZb-ivzC~M$LGg(b9N$wCjq'
            '=Tm?Umw08J_*}tlqc!y_~ryA{N4EV`U%JZQhD$i|2Qx)<Ms3Md^K6!998prU`iq=LjuOOBZA;uRwP1~$OPf_d5il'
            'xLv%Mdm&t6F%a%7o&Bi--AOEwK45U6fq5j$@Ey<Y0Pn3y=*;xEI)HJX7FhyzY)d?M>JCwTg`g!KT@j3z2&FxrSjU'
            'Obnm3=dNp8|w<F6}$@fs&a^qs`Jm{01;uLcdAvb@_uNUz@GP;^_QvT@49Q088`i$M|h%eG&i0rH_xf=doHLtj-'
            'zG-jxXg>@{>+XJS=|?hBrXmjx%_V(ECHSJDg(Y66Qe`}$z<R$(@mOAvPx8zF+}n+h<2*N6Ez2gpVjf;DX{b>ZIG@'
            '%1`w>#rbWiuZ&M0HtC2`ZRxie1KZ8(`T>VynuiF`2Eq#{P^JXhjf(S&*qoR=KNu()eVkQH)ApU7+$-'
            'fI~5F+W@C7@%k>bNBH)^0nR$W$jpy_G!Be2NCI%<~MK7SCAAv*C?Y}nZm34P?hcQTu_`ky}L<`K8Vnvh1;(RiFM='
            'NfSjv2=`qPsk#7hqM)%MTg9yTylMx>=*R0v%Kn{naH@xa|pA4qzL&Yu!?yU1Q<7Y)a%{yr{2{_R&K}+G>X+*gKHa'
            'N{zu2*iz0pi2d)FX<HVs(m7%+Y{fy3^oQfa!;@Ff@~1~{Qbh`kE(Vqb7eSyg+GjjSafOQ2%bFe?cTRZb-'
            'n{zZ)r&(tqi)}8Lfu@V9Y3fjm}6uA;gV-'
            'WR~6339=yk6B?$`t&&Rx2(;AqPYGWZcK2_E{h~fZDKnYy3wSuy8_u4+Z-PnEU=xY|=J%Wr>9?Zd-OI%$n>hqy-'
            'T{E9tz}~2L?8-V<m)dRzMb;Ny7Sngkkpmwq-'
            '%N99%!i2w$)HGQW`8)=H3Daz!ta|^18f;Ehq&3h)IuH`rh;ukmV1HZCH<uW4siTmHLz4-'
            '<cyeovC3irylFbDYSxuXUXaI%@~`?@qz3aUdCOa4v%gv0CD#*{C+790nkAFXx(3+7`@2}&jDM+8V=%#4!bXj!^6r'
            '=FMC@@7cXKOtcW3rZ(f-7?z2<A7??P^Qyu3+JULfwa_yGK^)E}cc7^v(TH4p=-'
            '1tC_OAc4#_i5QB_cD3jZ&n2$Tw(`orLv^77+BeL9<JG3JRZDNv#cY<6g4SGFb~dt66OVbHjAzadLaWW%PSW+*4c3'
            '5v&SybQt(%a**%tPd2+BK8>div3!DJR=smH<>I&3(58V^JtmNw`wq3|@AbuI1!U<-gW9KAvHnD?ugn-'
            'NN|W<7)LCJz$*Hw-Qq5NzBGEfzUdNSop?*uoHop@CkI-hKG$>6Td=oNRKJzLs~!g3u^A-'
            'yn(pbyK36o7qnE4L~!vP$JtGCABnth~sSK$?H|VDmHjg43VB?aNm6O23zv&*{QE95?sl4&x48Er+(sVH-XRfvOq;'
            '7Q#vh6T1YP~(@X$NL_4JaLDOF^RI@-'
            'R2?~&CiGJr&U<DGJxNaQ0#Knzr^+;0ZNMO6PFVqH|Z%{ungGH||VR;5c8PQa?HkSsZaBQ4}iQOUD`sZ>642rVozc'
            'z%HfotrOY@zI()7LzA`2pjUQARW6Ah?!mWa5U34Kf=WT4PV^p)keP3mMBBu`Z5{_@jgs%LAYF?x*D71$I;EY_Po!'
            'NqXkwTHoVwjE-oOvJ@lOW;N2~q>;)@7z1_HLwBI3M<+1IpHpJ2+#i2F`1A9FmrrxmD07)Ka|SYRd21J1hugHC&jG'
            '`WqQb>ql@<C)q<0Q)*>RWXKE13Hu^?Qtvqr=cWmq8!e6gA=FY%=pj#JKcq9LD8HWhFjg#8nvM+5I3Akt&|f=W*v7'
            '=2nKYG3FzRE+J>#reMn;wVI?R;iX6qkX$6@bOjMEHRdm7JbL+P2=N+?8IlKe|#%{KmovcvMq_pqKWa_I+R-'
            'AIl4wIZY*(5?7=?W$Xe7^P^wk`Hf%`DA8Nqj-'
            '?5R$%X+Cmz;`~AmJZ>ZwV!CDiouTTe8#%unb1<yu?XCDjz($4`w}MOAeb<X)MDjZsVu|D&o)Eh8b+1~dMQb|Lqqw'
            'VIXN-'
            '^n%$S073o;UgBH!02hGmJWN@G}WdpP38YRm0hNgv2JRyw$kPWZXvIfyFt<PtAs<ptD6C+7E6L=+HphT@+3(d4Ri$'
            'vj$#VI-S>bc3GCPHlH>4Df$aw|m%b^nVG0QGTlpva9}(q4eZJV=o4F(*b#$s9uAYHgfDdh4AUS!?-'
            't6*ssj<miaO5BEAp-8~z$Ln1u^v=6(>kp$T^$<B^E_AX#VfS{zF>1B-~Qv~;r-'
            'GqAqugk|_p*;?6!vNcNA+QB+gu9@u7YlV%fvoeCtgup1!%yZ2P#(EVqEKctq)bQa;!2+hTNSm~Nq2<Yj+CcUawI+'
            'fQlq6r<~`#h?OXr3tN&?;Y_>gDth4<RtBb=M#0Lb0@F_BQ3t(C0y=@0EQZNaj%#@BdMULX(P<#K`W;+rVXyggHNF'
            'hc_Mg`@x>OyEJ6SgrGAJFL#AA7`yYI9Yr$|<|w8I~t@_J#A2cGLIljF*aEQu*R2bLN6B!%+O5wd&PqwYXu?dYE|{'
            'G$n}GeeoI&oIz-'
            '5+TJO>FolOGI~ES<59b+yKg2U4+*S2<sX1&{`D+oyXxwc}H`fruuH8X}Et(r!oTX|Lgpm4`4+YkiM;8izAGfbn9g'
            '!Z#I3;sn2{UV{Wut@^{+UoVtcZWhEzY`Nffy*6t1Tg7&L*F8<<Af~`H?ZYa<e8Z2(cD$8ID)QyjUgVrMp5+h;o8g'
            'e(&e#H3oMK9VXEw9KKzl6W-N%d9eYWYH_1))n`3G@0tl<5X^&z+J4i_?w0?OjSH$-'
            '2pz;bt)T9{)h^no!3@k<lyhS(!JB3+S3{T(O?}ToD|36%0_`QoSL+dHW<J^9o0QG=;AewvdaD&k>}JbDuARfBmo>'
            'W6t=E8rjYHqGf38O9LmCA}FW~8Pyt+}TQgcLx@&*?ko&54%my1QR+EkWT4(WMN;+Crz>!2E3z+r_*Yq>fF9#Mt+?'
            '14sc66AzSot3M$d?6L*GnUp>Ug(~;bK3}Hd!~=fttSONh5+)=P9&^N^#xHGI2sV~DK14!ZuoqvXJ(|S%bBqxW{V2'
            'e-'
            'a~(wnA)J=3R0S_VPzLvGD7fTY}6Ef9*v|adhsubXLHbBN+<#Rc3I?kDz~59+5iMT_u(DtMv%YQR5+dyN+1~@S5Bc'
            'Vs7-gzA2b|wEoxOPiwR(^MrA42jD4BKUZ-B%cru%@;9)f|pR-'
            'nmBM9}#6ZgrsJ__u4M2EzNrwxjd9Uw5Nf6KFKyr>Qc-Mb;pk3)7vP~Ap)DrwL)?K|ETYq15g38rQrZn|#nbtE1jb'
            'O)u<AiOX_*p8L(ymFTwbl(OKQUF8n)@r`Dbe3mX`0&ZgfQXlVD-'
            '`959EUcfIQlx}ujoeRjI1~yYYr7zHwNKlwwbPnUy1E!&TFZj;()t0{zr%T4DFbweFHH2HhA{M|N0x$hiLb})f<}`'
            '#Ic^=kmw=mS0#Ke4d3#8WFmODY!qy4U)+7?VG4Hf4r$*%wqQp-hke1fcU=9<dfCOZ+Ns6z9%f60wX|P%320j|=8u'
            'Bgfp*JvZev9=l#jd&n=~K#7WH657O3GZOS$%-Ix2uPhRp6*oEUu@Gw|-'
            'DoY_>9Wpi1ZOO(PvK#^!J8COSZot4wIqDx}IIzEW>#jL~9AK9*?G*A0L|HFz;)kCU0?*u%A9!IjrhHgq2Gm(X0a3'
            'KexI>3tc#7ZQQ2GBvj2P|dPjj>6?ipu&V!!K5WF}2ibqIu?6%EeLNvc}8+fYdSgP*R(_lgj7iav`6&rM~C(d7e)I'
            '*UPF<=e_5g<R}my7jle8H9LrOjOr#(fC-nA2&Z9M7zJV)H$D(B+JZHjI!fgZK)~C}7>N6o<(g?g5*GZ-'
            '0HzvA`@tC;f_rniMl`xQH*{nUJGQhv!g|ns2|EuhctAKdVWg7#g(t@>IWOkqj;-'
            '??DE^$(k=FU#8}{B&ww!^`fv`-'
            'c1EV)fvfBzhMZluM{1HJ((;?nJ8nbEt>&fb((BYuRPYS?W9+`cs1UROblj=gK9C=R)1{l`?{8Lk2RJnz(QW4_r8Z'
            'LZ}onB3pY}h;l67iJAH~}CF1&Ob>Rhp9Uq}die4N(h?VH`ot4}t06=}Gcv_tEbXo^l5<!Lg8NjUqt={-'
            '<M;!)$DMln^W@H|SfVVW&aHKUu0Hff3@kbSG|#VCJ8APQ4CS|71bd8uX(8DmD{>r$ReMIF((%0Vyv6AQ|4rP^4DS'
            'LAEwXjn^ZLFC!a-%7(L9p)J`bJ~`{%o6zgwa5N5IFmM<HOB?y7n9OWyL=k|blsPX*H4dPH$3unz3djoZc-'
            's9O)^S<Sd^8%HTaRh{Eo`ty{4DoNo#%73MJmIAe>r%&7J(NkmD@Xu8e5E#tBlYV5W`L(_Q$M*=OQ8+by!~K!iwd~'
            '=u(eTTrJl(ax_ziB6ju`+v9#j6Z1sm=Hm=mdazC~ByUaZ1g}M1EWN0*QBH3Tn=Yn^u}t~8R*%o8WuHR)GDfBsYco'
            '*~`sQrTugW!fjp?gWo2+H*X7sxMs1oV<%4RL28eU>H&#8#H2Py%Y%*1nCO*bWqk7>OToMHinv^G2xQ`wBRAiGVvC'
            'zk@m!Wt(f%k|Lumfdx-ZaJ#CKMI9f@kR1=aug%85ruGH6cy<?5MRobz?dC@F>+adSCr}IdZXw3PmVMSc;t^*u5V)'
            'OtdWGodqp{c09rXV=ZkWxa$T9pi)e7^98ShQCH$K9Jkdc5UGfvt<c8O2ys+|j*mc?bgg>^vt8xTC@RoNb-'
            'V*n%R9GtJ7-sm^k!zob{}#`tWi*s)C1Z}9S(@hi_y_aKgx~2r{oaEoImjn-'
            '03=#qrR%w2OfP5NaO@_g2ZKFO!?B9%$0R2{FJnNOoBVuvb5y+#fn0&x8mrxf0UHYD!0N?;I}~Z>ILY^bpf$AV#$T'
            'VKDh&?NKuyl=Vgb?i7gQq&k3#!=#ILwmnWSY&sUpNA8oSYZ7ir%_^g+lA5>EN<G)cpp5+XwDs-'
            'A5Yg&^2}t?Mh~3n<D4^>=hVMV>KV@;<q&uLUt)PViBe46S&*?W}rQ3&MAhRsn;X>lj~b$}#so=2k!9QZujLxPiGP'
            't{H8-'
            '!9=XcA?C@EblHM~CJH?8g+Hj(e$4c6+c^P!UFaG)56tngnYpvm`j9)AINCL(6n)^vU_1jUV+_wEOfxv2V3sBPOLz'
            '|0u4__|DN0O22uSsMz0<637DXbiu<5LHy+U0)dSGBuuJw&&cou4=a5f0JkWj=A{mx6ztotwQ@WS_XA!6y`eiF`90'
            'yu&KA$-Iy7KD^b-'
            'xk2a^pG%QdA<Q&Lf%IN%H(2#mTCZ_$nPi|@^&QTh&)8XK*aJL7cW*TiKSV@e`v~aqvQ=b$DqxE{?59<^6NUUDRWJ'
            '(-WJED4XJ|rPQ%+P@Z{vOJg?uuODwn6tWol<uPY!7>I{=74;~~uPkZo7BZjlWUykUv!{EDy579s;I-'
            '6j)ui?fchwJ&Wt1(Q60x?FuzF8KLu_Y9&!Mhek1AfH9ObEoVh`0vTSzILxeNJH!4rsqfFqsUU8?b^RbC`YgYmx1!'
            'Dhd@-q)-9()r_O-ydU0j_Dg}a6H?`}n-2dw;DTv5BdWn18X2MrJRY12j-F-'
            '|+QQs}?JQgY*A0OEYcaEyga4&{gVkaLdC0G-'
            ';;ODN<sq{v*c?NYmW#=>7^eS2gwm)F|L1@IzxXM!rTtWzT~@^yJy&5<!&Ulrvh&y7o!_55fF9m_<0&wh^Ll~2quK'
            ')+je$j~Hew4+j{S0sUt0-'
            '98UAXd9HO6c4$a>)wbYmp3}YKIk#9(8(2O=t^E1u=|G6xHslvGuv65t6UoeqTv8w|4gof=M>h;O7kMd0!97n;<fB'
            'VVXA&xk*7M(mu_-mHQj6Ow0Fc6+T!aYfQ`dnXPXqFgN<E4<)#OP$>;U*LVV(FnoQ~4?)HUXU#Uo+)-'
            '!;9z&AD0cu3&t2m&nO|d@1nakbO`s=o>DOe;=kdMk+E;6<)pwZaTB7ClP84lh60lK2b_YqXttgEh7dvCL94Uv%Cb'
            '2pY-'
            '!(PY@h0m;~2O{%a_u(zGDELm@w+=XrP{Qs}Y@?jo{|xFUDmQZQva)*g4N5ZTcw|En2qUy6v(N{(q_A2eA!pEL3+6'
            'WgPjTNA&cFcA7;6d|uTH+$4#e^tg$SeOZpzYs5l+kBFxi{gt<`4D3fWg+Uk8gj+&Q3{PNtBFESgaC(fXF#<pMPKb'
            'kEW?RH5L02`k0KesK@Dzh75dp|Owi4_fJ#RqjmebaGBR=YUwnpo~mRin+9iE+2=?r9Nao)n$TZ?fJUo*5hNKCG37'
            'n#ErGK~%4yY{|p%8r{RntTN8f8r7D4g2@1e>+VP?Yw=0q&mS2p8hVKe6M>}ZfoV7WcwsjLSuZ@+7~TSmQ!oA%??d'
            '(J3Lpx=kah6B@|#5HAOy~{vl!pT^|j-'
            'Z27_v`=}EhNoiDPvC_d;#LgPQSj@ts7qa;kT?kLhrTGcttr`Nk(b%#kUf+k+kRY@dP5k!2e}xTD;(VVGkX9~R86D'
            '*F{1WThnEokjXptl1ol}AhOjlHl;pqovefY=k_9erf4ga|R_F(5f&NAlpM_M$n))bRD+<9=lIS`yTukxRc4u8&H9'
            'iJY(dYK<QKRP&}g#NeuxXwYuK-'
            'E5HyG4#yLC7%(b4%MvF(qOa`~~%O;a|=%na5;xlf*}CZ$d*yn}~o;{*aRDwAcQ)WoR|QUuY4*Ur37)-'
            '&_1=HDt%0F#l?=Em6af|IMHJn`D-'
            'RT7MJ%OdARPKwAj?Fb5$mxSSgE;B6v5!nY)TF2SD_sP4SSf%1emq;$<Wp}zG_j6{}wC$?9=k8tfK4cq9VH|wo2#+'
            'j_Gu!NhM>)yBYPc7glEb%k_#-'
            'B)%;^yobQC?ISi=Q`}ImoXx2y|ns&3XNSNCy2S{{YGP0^U*lCsPUfCy>}R{8PUcKu3vu&?6UnL=8Hxi4Pf0BcxD{'
            'YU;pN<)oraf492V$QaLq#+@BvLmS6sx}ezeBRSNVK-D?L2{#UejKSk^bw#_;-QMmcJLn}YI-Pk>jJqom!^KGbT6w'
            '#*-'
            'Y?aIoERH+S{w?5Ao)Ao!ojp~2&mG*g_LTf3}SYMZizTn+hK}+GW0>=#MHm8)%$d_gzJR=O%YeZ`YY7xsxjkcSL3K'
            '&i8wn)ximsAP*2086S7;Zc*9C2A)X`mFiDzvgZWjKE2)??DomgfMs^KojRIC&1gKD0SOzHkHYAFcW*v47a||VEA;'
            'zfhL4lD2Nd&Vcc8E8=hwjgt8Teas^@i@o!8Z#+N>e3BN=W0QIch$gpP0s1n^Z1(lzg+hJ20~28W`paWPavEJ1@fb'
            'n^LEhn(B;F@;}b_`>IvHI9;#1d0;leZ@+dgE!H_)0GRGiG^n=^bFO`_b?^Py!>IkN>t((u-'
            'WQ8zTV<4)kOt(A<#QZG?9I?SnmR`cIF%EU_k@~Vub1<e=j(F4kfE2hG;$Axp_*qziPK^HQyf0E#T8$1sO<*!Z^r8'
            '>*J&=>P}W=7_=q|Smv&`uS4FlcMV~uzmp+-OT;5F4`D)+cA-'
            '{zS=RB~ygy2lHS+Z3Jf3{;a(U|+qx4Qw*P$rJ)Wx1FE)kU1@I1X(8L^Mx5_fPE%YYv-rK*gY$;*NqSZQtpUb0_>D'
            'dwYN;qB8d84pIQwlHRI)8%9HOA}1ua^-@QtH@44Vdg7%E<&!n&x-'
            'w+MJ4C14^3l)_$1pkvJ|~e#T}sV}*Dbj<uibA}cWJnbiE(m8kqAQLLWP3*j2u@6uO$QrG4wq+E?0W_?0i@U`=uGL'
            'XIOHFf~1sU`x#2OBeF6#ls*#+n3x!+eC3f{v;Bzx<&3>b1y5WiYjL`^OHdeGAy2TE+!`|>ZV1j!RSB_k3s9w`I6w'
            '^jqOM{VRX-|zi1A4?K^DPQd|Z@mcM)k6O0B0q+6c4nki0>d9oV=3^b~|rrX&U-'
            'CTHqgwxlWDSH0fuo>5Sv9E6?@oJVyX=X64OZW8}iQ&Z-'
            'pDG}!()q(T$mH~~)cxgp<{@c<=xnSuPvVN(@Lrys#v2e;sxmXpG*^Tr^a#BD<7xJlLC?yob2-'
            'a^QzHRg)S0QtlbS*$KM%J}^kPIK~x=7~OScJpcZsyk{3dgb!`N_~XU#~p*gF-'
            '?{2(m#qGTfj|9r>6wsNU}UZg=mDom`~FiRiTAI5-2eVT05G%jwr*JQ1JVQ#+Pr+uF{)Y>btel=;rKs@bX5-'
            'Q>kXmF132HkeRe1srGN<f$$&Nu!e4EuKo+Iah?i@Lh4UznEN|&(Jj&&J>6||1VH7^zeO;N*hsHj^qvZ;AaJ=dL_w'
            '7IZo(lRMtdR;<WXXaq-34=Qf6(KkGfY3}JX=2jb7pc$g{nFv<wEH2~6b&Y{?@hKHA&tS?vf=7N(}dkFsV-pVa!kS'
            'hg};@mqJzb)Tv<4``!LoUiGG$m)RwQbF@*VdrWSY1hUH+3B4#YM4-$ah*BB-'
            '$BddI}JD*V&I+8NF~zJQS<1TRYd)scdV%`bwG<V>z#n_-eXtFU(%FD3=MqZ_ys+vc1UyGNLR`=X*4a<QZ%$A*$q#'
            'trMFI9k$IB@HY*Pk+tMoMsjBOinN|3v{g<ap}bED)W)D$EC*D3YH)sGZVeJ}Ckw!ziy%izPbJiOm@&Uc)+@CtAFS'
            'Ph0qo9uf^~nS>#lm#MOe~A-NkbX_$H{Z35nb*n_}_4;M|I0xUza*Bk1eR8q-'
            'LNkUSuE=yiEb3cPXhV}t2uB<w{^N%RRPT3w1{kzc67KO(1w2yf+xYRv4-'
            'FEB=ma^;$PQ=E@R8uMPpk)`#(wh18FeuHa{X;fDpN0D@!lbB<gdH$`vREdMbX5|RXk8(>>-Ki{pUnFm+z$IYPq-s'
            'iZb$$J!s5V~<rMc<3%g?a53>0w1i4R2~xGzvdDKQV?hz}fb3XuWGVu4E}7Qb9ljOYeK>(6h1dXXahi0Yv;PbED~j'
            'n{WzMM0?j$wZDMSIElKtF<M~HCysZuGf(j>&UK`O2<K#4$_DaD7Z4P!Fi+0BPFGnIki{GPk?Ps0p`wJ>nO36?ZU$'
            '#(L5*zncZhBVS+ctas#gVFj1c?5KCrvW`z^2Rh&21v~|xr6es5%ug8TxWm(eXM3n-'
            'I503O(m_=?SbF!eX1fsSdx@@3k^gx0yKnI)XI)r%Xwf_On&A+CSjfHnrG7Bwk(o#Z_WV=1yL$aDA39CN+JgR+`(e'
            '>+&t=0;%JP=F*r&UD-rzD}x0uxCHf;R!$SZ&~OB(pEEkY4uJkQRyO-'
            'X;@>L}XQV%A~bwaVT@kP&b)_Y3(M2;b#P%5XIzq?yT)nfqzniZob^-'
            '$&I38J*0w`6YjyNd%Uv6<8q|!pdW`E;f~ER+pSgVFsBR4#Uf(kHV{VTdLPRJ;V4k2N}M6f7K9afiC7_q{hV$i_pm'
            '@%&+Q*<G!_7nA)LhDQm*5*S*adXIG;h|uSy&94D6Djl|4g4jc!F^bw*>293!uxv7w5j<SvS;r#*C)5ifyXL|Mo9+'
            '}C}?55kJMjR-H_5MsKr8@b$i!c&L-'
            '7dzcKa$wZ0&5i2wmXI>mr>ew@9tl;cbQuCa_B6t7L&p1TUj=G;)_@3LI#(8bihHdrCO$jM)dIAp)P?}9*4`mUM>i'
            'uC{Q5eedjH#9+nbO|0rPPu;#^(zz8>tsej>~Rv5+ol9B_Q}h{EXLF;)x9yJwpNc+<)n@M(R{0!c7}&Sx={b6mKv@'
            '`B9MV$`<m>A%)R7TX=vf(~Wh?Cu84C;#LwWzO1tK$3ffjL{5-'
            'y7qSH`dFu~STJd)b5|b+uRcy*AMfZDrZKj|m*0jKom+2Cm*bc27WUG@|2*0a`Q{kTTHd_2vzGg_H(G#RWj1<$k%+'
            '=9tgU%pfQ(XBJHpR~?)Uj*HBNr47UjEwOA`P^MrXvba%TJ@F}=EmnW)J;;%rF(pGAGmtQ=YeMRYZhLQHmAR%4I<$'
            'YE~Dyb(ufWtulz-'
            '7}=vL>wIIPm@)@z+yFTYh<z7gQT+ZL)NXE?{FV|!K>ZUEFilHLWF0=OgsDNznwIgCJo~|Mpy7e*s%UYK7L-'
            'AE6c}^^f79gt<VjEO}XO8M~CXvTb_4v^hg<XwLUq3-'
            '~}~8M!N;iTn*&Yo$dn*+H$P@<r)=R*NBzT^L|MNS|b3xd82s;Vo!#-4P#Z5M%-'
            '9rq{uzC2uU19*KoCmGM@fJ4N5wCX0qa^9Cd{xM<`6SXYyTr038Fiv8T4Q2l0nZ?AuvX)UCDG4*Rfnafpnf?JRH20'
            'G62t93Q34P1Iy3qXYbQcNb&{<LMqnVC}qp(wKsU%vSYemMrS}-DYXn&?wkvU7nW<%sMAcXm}0Wp@{cA-vGTr6CT?'
            '8@Ku)Ea#IwFhijOPTTP{HzSP_KG;1ni6IPp_{bWwf9l1)hOS2Tyq(^frA!&DL7G0%3vluxGO}w?d-'
            '#U9=Wy(h=K|Zx2q;)?bNi%*!Ta+62(O<Nmv*61g?e<g~Jp6VyGRT8{lVF6F9#<-'
            'aSFOf<xH||F;HFh26DP+lG)>>_d(u~};^;-?TZwr#h>%=?2vW7Xg~Q};O@~P<ZPhh2kjXUC?d>c<y|n4kXt^lT%-'
            'TiK7CaxweRw%T_|Wg=tcX-JcQjKWe?=<f;(&Eq3KzQYPZTeGUQ9X31!t&DET4t@`xW0~C5Aikmdg<K$reBkw!p_u'
            'BT#xs1txVz!5_qsP9~j&Gglk5@yy0ComZ}5!#XEW2S}IGB9tk^N%S<WFDf9L%;?A)F)vrmdWS~Z;cW60`d?O<_L^'
            'Ntcmi#!+4418W7b09{V+5l$SIe`FpDHtVtYF4sj$DczN6bQtvdQEZZP&E`B(CHJHmUI5)e|e0CJj{dEeT5i^6NzU'
            'lp~(KhPCH{%@rQ#Iu|(u)g~1HM%cQ-'
            'v5^b=!4C=X2=_M>vvUs4ft{4oSrCV8aYJw;0SqgEasQzLql=7m<OF39BUY2{Hl+`u?jQk+qj>5a>Rg!#wxY4u*Bq'
            'OXr7P(U8rYHvG2gq2CCuqWdl=2Q(H4L4z`9IZyjYkN?t$5Y3zj=Gw+*!!1SWI+1idMHvhu*v8ZOmhOvPJ(AD_MZW'
            'dXO-6*;YyBPr;t0pSo8#-'
            'Fu0&77X;l%^eIeheOunGQmy;+apJ*eP%4(X?SSuYk&bGWBiSdHiy=V}Q3tkbNg_^7E)solCh=X%-'
            'steh<BizaS~299FIs|ujAxm9YHnH}q8uYQyvQ+0y{T~u`gw4l+wm4_9n)y3LzkE-Tea95fut7nr%!e3SY)O~v0P!'
            'k2b{agD4?j8##2>S;Cd-&CjG?7#8-^zd8c~x<U-'
            'U((=Za_moDXR_6)H*s}ku7quZ*RD9Z<SERy)RxM7?~D$8Y9a$R!rSe3!IiN87OZ4iOf!c)o*WmV$bC^!xQXMH<Cx'
            'uPy3+L>(L9{Wv>ctlBaf3?HPWTQ452ZJ7ko%j)W)3yo}-'
            '8%D`Cu!fX^h&Z14gJ+dRyUZ2c$#A2AXI42#Hlh}^FDemxnaT@rUnbu<F{1z&d`>73#45{|CcUzekgBglcB7X8orG'
            'K@g!t>MNiF%IP*lXm*S`sq!QXmHPgdD8rsR^A&ep@}E8r3l=Sot4CoM0GWG3@AhrD<$C)p&3y|JdV4f4}4JL;;z3'
            '{Fh3+zA81MA`2W^DX2q)FldR7pDQ||4us-'
            'X5me$IGdJlpejK`?G(nb$ry0vGX=~oBPk0%6Yt*e=UC~>@d~4*2n0ZQix|;-'
            'NohvzlYNhg&VHduL)P0|a?_5Y6(QA_V5p|JsQA4@$freKhy*_FEE~RF5Lz(pCqn@%^xizFO6xP>{g!5EDm6V>pSq'
            '0qLLYQc0aZ~pY1&J6JJ||rc@x)}?K*7UhK(oERj)>f&uLa0p8%WuLbDOM$7|rfuMML=LGf!_x6cc?_Du@6C=jrga'
            '2e!$p`=!Bhd<jVR<(KFjou%!(mbqR*a>K$`7&F{vk{BDq2BR2TG;Rijv;MB9d^$EokDj(Ct6EqZ7XZUJZYZ8kChv'
            '=<G;2WTbh4rP+Y=yoi-OojQBJafUP|x-@CAazK9R-'
            '=g!ttKi}kH9_mX4yZ(A9K1vr`lK#YFl^F=*Dy#KfHZrs<pOAj;xpbUB{Y@XCt=k=fJ576fsK<KH!>(|fAsyLjLAW'
            '6JF-ZYmVqhB%hj{$f3uW|8V33PJPVC2PE1doLDB?gFuZpHW#oa}m1nq3|~8t(>l3=!=ZV=CZ$4oj28AH`kEbulNG'
            '(!5@e4>Sx8WV`XfLH-m5`>`or(oj!@sN|CenivsPQ9Q9eeKdC4B^-^Ly3aT+Tg`=4APYEB)l#0Z-'
            '44st*ZFz<LA8@O5>|CF@IJqqi}XmyDB%6rb<fj;+BFs;l^HyOIx(}gAYW#>l72m!>1BcOY5jZHDmXP`8trJ77mJS'
            '$9{_Ry8vGa+p}l^yaz!ZtZ*-x-'
            'U^{v&;R6~9`j4(wWpocrG~EE5zp{>Q_I^@LV_+5SB{`=a7;YSFjL0?1x!`)>=T2p()!HEhXv58=#Y>IfPd$nivn)'
            '!Y%6<iORM1ut6R&m{hJN-O2%5&nvEt*b)j7PZHK7;Q-'
            'VLU(X3L&(*pC9Y@%Pp;dyePo$$YYd_%yz%;r3#=tO(8fIDNOnvvq=WFTU-MK!;E&gV?FxAKW6eaSIi{VdTD#h9B+'
            'K?8Vlt<R=DE(P*L2Z+kcb>V5SJp_}t$5g5dLtD*zgMuq6Z66i09FtNW)U;z8=0NKSKLp>9L?&`N-'
            'Pjhyl{%zA6k3?`N@%#jaFkh!&SAH=h3dq+*j1+%<;v*?h0<hj5#(k9nW6+a?T(Ib=o+xOmtwEtQV)ru!d3h-'
            'BX%A|lB)$zu7DoCAOOT%k@7~6sw#U^m0I7w4LNkz%@Iy)W;+u__S#(3w(n50odC{&^wdiQyyw?(RN>yo@SR}CQ;+'
            'OVO%j6m{70mEfy7OhGv^||Hp&wmrO)SudEwVfBSv9EIJ#2+)zj7p$z`E>%tPwF;ai2Si(_Xxj{<{jWM^Twee~<{x'
            '$|9qq)#=Qz0&DL6-rHA$w3v0pQOzuQ;*%s)R|6uEIdAF(a1E$H!Nuswx}xb~m`VJNyY!ADGq>n>)|uOlH|b-'
            '*kK;V!VY+e864TnZ;jAx=ccP^BoT`aXz3$4IBZ7Akx$hGpgmW!lDgfO(%f5MQjV1TJyUs2HpAD+!vu?$#FF|Y7aa'
            'g)kR-wcxs8pewMmf$XV>bo{I3~9UW@_JCm<d*CLeTDITbT&DwI~Kx?<AH%op8uVw>6ADr9Dqu--hu($6-'
            '*h*EgKeub*Jj48zmBdIv}<ZFA9dC1(LIj1JSDT=bR}zK=1Gcbfh>EaYv*nnupj*D0sBkB3@y**xV>xO7`f)n|!#m'
            'RL251lDvf`R(pV#oFv8-{4>MJNVb5-MjHc5dgh$Vx#0C1*aI>4#spl$cRe_Wy3U)Ol7RV&!a@{-'
            'b5EXo|y!NMW7vgwcnBWfcweS<ioIIVWY$dZz$Kr)gJw~%%2=nFLi5?J^NNCL7TJ18G7Fu+rUT{QJ1aT2ZkGtLzd+'
            'p2|RkP^Z_pQv9O`f$w^A5>}aF9pUaiw^BjlZewCw$ilI#V#4HA!OFsPxz=F0qfIgN9dORhWr+7%QeQuQYbRv-'
            'U;TYGl*S1cf*-#z;p7%k-'
            'S0QLPk5(=Aq+9JYsbpK<by8?%qYjf{w+1I+Be^v=a(l?N;qT)u09&ho52~hxf=$pinFT{*I}K*r#;C>;F9@$J)MV'
            '2PFX~xK#CvcDW8G8y6S04baCf~1@rs{NQOIGstS-'
            '{dE>dzFHc~%j+Q*j@%vq9!M{#60F{mLi4zp;s3R7rtq`KB56|^ZrKv=HPD>G8kw5O|3dtZpU(!5w}u+{<2SH<Mrp'
            'mS){*93tYfo326e$c)tm+{{MiIi==3HmR!2nx1UKWoo0(k(Kyi4Wb|AeUIVAaaXU`-'
            ')?QkOfJhzJ<WhOL*9pPw&IG_v&aJ>d302-'
            'm8C0#tF+uJ?(Cnb+!nLMg7KT#W?F|_wjnLc?5xyw$lj(JS3B+GKRpSj^q-'
            '5Pg)_Fkem&3{WwyuI)L$Vq3=pGIjl7o`-'
            'x)vG@3v~dyaC;tTlHE`OUBZvnN=KprT3e7vWjm*HJwwy;_HSVuJpC_tCwC{R8>=21ey#QJh@XEf;flq&yWPYObC%'
            'ZVUds7qi_$>7{N9uz#~`XYt#wVw9_rew231D4T^ox!NYW(Y^+zEp~hlEzdk~6w3P|ZX))jzG{{XRiYD_GLKe7+8O'
            'mJ3wD)BP-H86$$^}04%6ZR)8a=$J|5e|+-'
            'Qsv4uVA_kihmJjI#==9oG+4qsECH_Ja8e>am(s7f2yRKbUq?VI+S0!{TzWx<6`t=%t|<vi>}+1r&U*o^Z0kBOFJJ'
            ');U1@t+JTId$NG{;>?VajHz_C`TOu;60r@I$_|a|q7;8ShNy3_VvwCP*u-weE?q7r)8Y~kv{(h=7lU2ab-'
            'g$(mwlSzW7Uv~qwjjw-HT{pBx6}koy!Xxq(*}#L%#AMX{oB4b^uep3r<?dXx({)s>hHxSI()izD$K-'
            'mORknQhtPHcQCpACDxu^u~9Cpo$$nLRrj`8-BS>a387gqy<>-'
            'M>LYDby~$ie&1l=HOz)Y&{i#v5O=`w&YgXSaXrq<dhf}Dc$8zS@Nx-SyO5SNC7$!De-'
            '60J0;`au9?n2n3y!AS?2p78}%d`?dF_*0tiCs*u;bg~iE&eVT?6TLX$~PU{t*!k-'
            '`t*G^@j`Bd7tr5L?cTxxC(TYMkWSSyQrQcA=3R04vTZ_+4+QO&ZlM~3#ecD?!P_(c(u>XKrjgf)e;lejT~_fHohc'
            'QcCXt3U65%${;dn;HGx9aSMrTG+FY*yAK1`-'
            'us+AH$?KGrGhigkyCF@JLC|8pk5@}`bQ(l%1)q}s;<+yjG*=lmld)YIVhHejXC|z$|`7^`h3jAu5BUW&Qz57!1-'
            'fFA)qne92Ib4Qh2j~Y7NX%V?Oj6buV<4E)X>J&f$FwGt+Z9%a<ZHWy<8vTjCXGq<%nHC>9Qp9o38kAGS;^-'
            '{$xnEV>EE&P=Yya#vpOszF%jlaRSg**!{$jZ<#x<P*LTk~l58vNkU(MCR3eq8$gnK=*>P^*k7LGngAXR9DY2MN<^'
            'p4=F;&!QgwZK=m_=-<FiFjxJdm7gTLIPhEN<WaGg)X)R|*6Ss-jf62spl2)aO{5MtyHUK)?Gc^&`*4ApHR-'
            '7c4tE2rH0P;HvJbGNT8)v6)s<+$rqKBAR$Ds*C$n(%y!y;_o8aoFc5po2#Wr--y?3L6xnUKJ6%CcKq^te6lfJH2T'
            'mjZm_0iu_{G^!;c`Xe(bL0kFz@lu8Ja_he2u@h~)(`3cXbJLB8^n85R2U!?P%{wjV5f4H8E|?2?U(Ru2F6XHUXnW'
            'E@7H6g4WPhZqitG`<f*QBF{PMn(7#Q@7*|=DPfDKiS>VXl~KB-'
            ')Qo_7h}cMH7h;<Wo_D&UYtG@O{|C1wx!guR%pK|=9`8JwbpQdNOzIYRCN7O@rn9vv532E1s)ALF}6CQSOx*L;gE~'
            'Y5I6U-UO&TZy5fxz<e*P}gb>sJhkb>r!6YgcTP@06<_2BJss3%#$2RR0Uo}f-'
            'Mjhb=XBeN@*>}9*aEsd0S~37=H4EUThj70!R9qC?<?Clv3;kTgG@nm61V98`hcipurwE~02lj~SVz*Wr1WJ5`T(D'
            '6p7U?$7X-'
            '$mpl~e&uvQ|s?qK7Yb&%0|3Epr;1Wwv@2i}m`AG3D&{9TjBV>Sdp);%qzzvr$4?YUw+QUb_42sLX3)+`j#%S)o@W'
            'G$!Tnu-mS_WvUsS-YSsUd(6VcYE52Way^Wl-CR+KUW}q7%?|6(J8*h9S5`xaO2#jY4OyF3QP^K3|Bli<N||<{a-'
            ')V+GNB??%v@0|jzvACvY;ZNKU_sI7+zsB>C7em+hDr*8G!e<y*7E@%JB9fc)5IyP-'
            '|0{V6tCE6JWcfe?e;0=}WU=76>%8qO%9CKF5}SB=02!r*^i>JZzKm3WhkeC)0Q9*JBWgDjrG7KEXJ{0+?r87060i'
            'WNz$*_u`YWBTm==Af|lRf89L>>?z36oA$MTtATfydYSkmRj$R;uOCOC%m_4T1Q<>L&2JjuF!3*)Pu+Zt{)9zek_i'
            '<(r}E@dKdfS$DSr?pOp@|~9G2V$^^1hk8JzqI-to=(aFxFO&x4)+nC$#@cjx!xeCO-'
            '|qC}ojSc$!|Or|JIp<Qa1WKVBtSU`|32{FFBGk5`|K^re;^VETgQM3K?zy*cZ$$L?^{p(|#2@7CDqvmf96thBo5G'
            '+;k0bUGwam90_0vCtS(%_7gJgMOE<g&)nKNBsl6Q`oXA!S))<_@sM1PCRXCS{x?y0U1%U?o+2w8gxvU!c>0?WwOM'
            '@$+IE0R%17a5+{6GYS4!T*VOZv`FAHI_@a;{PYF?xXW*OXtPLzm<)@h1eE~-;;Z7SeqZE3uh%yoyq&-'
            'IOzAyT^Z<uSu=<9s5@SZdVlw^fOEgxlrFN7mbCc@PD*EnB>;~sKKcjdGe^@M{oAS|O4cz{#E9%~=Rq;kNvltEr`J'
            '2PzS8q=9=Z7!9Km8#;J~%x+eDjho6+WLRJ#)A8KYwYy8oqt7bN0vKANPKlJ;47S|1$e3`{RG(|31jz!`tHUjGExz'
            'e-xSeRw?!5yZOszclZ2T`0sDdr@y3UUuE#y|CJ6hcO|E<@*iJd<drz4z2xC|xA+}%8|jtv_f&rPt!yAad?P+=#0U'
            '9%IbGFN;8SCLtK={{a-605qSjI_FaYe^@o)8q#{N=P^!IOfch$&cHN6aeEE@Oom+6<rmpgF-'
            '+=q#5H92j9>QXcuV!W47*@&Mw+!%15R6?5c)D;Lp>jbg1zz!39gn$ZPz>VR+WROaXQQ3A6FV^wXXGRV`u4W-'
            '3k*VKUe9M&1Amy`1s=P_<&wvc#GYtof$CP;6Aa;)Do5g~f4CNg10&>ToiELAq9J2;3#uux4vm8DOx<xQ6@6S#cNk'
            'M)%lqKMcE>Y85Go7&4ChOzOH9X9+<SQ|NSC^Cx4Rg$mSPXfPpwWtMH2>~X4aMT-GG8*Uf=|iFF)Xz+ry%qAmV<yh'
            'CUb$hjmrZ{xiV43Qj%MqRehjW0b}rZZ7#!iYoQXho7S5JvyA7+;1l)&XaPw#S7U>_W7dimJg|<y1;<xRNX%+f9dQ'
            '4Y+ZHIpQ;j3ssW@4__ncKd4_<#>iFfZuLX|s(2V{}ctplDJOTg?WPY<6R{P_G-'
            ';`;Hyn}ZjJaLe+ihfj`P96ZmDpC3FqJPGJpp3y>xawxm2ARJU7afRAF<o2ml;&h!HoIE)?f@9(ZS`ViNp&1-'
            'yEqFw)w!U`qO^vsQ4SLOYQQK=b#4it-wdsAxDNsMXYcXCT#=F`ygq;)gm01@c^Dr{*0^J0lTwG$tO!uf2e)gp60z'
            'nwYh}QTofvY2Dhl)I^=9b1=4<Zvk3f~>Lf8w{j@vS}N-'
            'CT%L=<zvbr&_ElWhCLFA@G03E5U5<BGs3Sx5su<u{l5w$yCE-'
            'X^Nbg{#@T2>|b3tRjg*^lrjr)T)no?;1EL6RQ{IDW=a_Pm%seH_b|D-'
            '8YR#79>M?q<u4i~Y3|vcGcK|tcLOa{uhv{-'
            'O_Zr3KIiS|@frM&kUA*kugnpjd3D%uh`sjuWKDrv=Lad>PYK@p1aF$3Jh;+5{=VmaPyK{<VziD~+3Qoj7dWEWqZ('
            'k8Jj|@-(2hh_HzB?pgfG4OtH`XPv*bH^a5{&#*yK!(VWJKHF71QUx>!vED04MgE)i!|lWUy<B!n_-FZT60Vm5L3b'
            '_geQpdoxNz8!&~Ultqg1uvM)R+p28v`6$qif+_R+UDvY*BW&9A>nt=NI)})1u%|uS{j&{+_#%>nFBShQR=|pgsd)'
            'i+oir20JrwIoRk!ji5?0Xi0!;f>?HYY+OIk8oUc{6vMVVXr-qG2$&iwKjA&^Yg99CE@kcV2KXNyTv*Wx&krN?16C'
            '5=C{qQX7zNLnKkryGoXKg<vc?+Gk^f{ESl-;WJDTdEBx*x)aGgBO}s6Dq7*S0CIHVf9GyLY7-N~+y{Z%K-'
            'u%#!8id{Iu56E)%s=>8OmzGlVP^STBc!YxU`h2AMe{sqBkM+^=$(hle;!1h>9L&(=yg#yJV0~uAQk~|f;+mShV=y'
            'c4&72GuIpy=c^zq;65k(m?MJInxMQ(DzQHG2lK@4BdFKLR6~j<P=Hc2mvMNqc#f!>`mDvQJV{+BC%bUBu+V9%cF!'
            '#r?ExQPw{heV`{q$Wz1hQ5R@+NND?0pd@8MWep4w8)%BPv_%^uTX#w{m2aWp1ghsFKTshac$o{;-4xo?Um8-'
            'N3QmS6v;<}`lRbRy$XD)koP*!-q>)+()PSPNM#vFgGr+VSf;l-'
            'gL&8L&RSog?Q9lIP2lX2EQblZ|hOkr+?Q_Sp0WqCK^0gr!D-'
            '^NE@KhB}gN)fxT7y6uE|MW+8=Sgm#P#siRwMCV<gv=NWjDSnZ4|!4EsY2EV@4l6(a_YO8f`UR?swh_V|Xo{xx>T`'
            'Q!8_+kn2_x+t83xyW@B>dk=s=b407O4R;nESmADbp;ElJ(a>p}b!){%f2uiTI1<?7j9erM{<6r|^<tki#SeE4_k;'
            '7s_~F};UA3960#Nasr!3*U0&Zm}Wm3Tv?MVSavnC^6B>Z%OS(#uhZ|MRZ<JU98Hyr<TUBkI+a(#(bC}}j8R2Ny=L'
            '|jp^VI@mjIvgR;$~C&M7GXwQvn)TqkvS=}prRN@Gd9#smgzsNVnRzqxzlu9c{AhAb;3Q8;HeC9DFNV%=lFRXs@E3'
            'sNdtat=oc?^bbhA$tf~bkp)qg+8rsNYxEkIlQdLk+@wQ`8XQP&24J%ox37lB@MzLh+*UeoNYRkY~efO}jRCA(}k7'
            '0O4bmKi6@&bDcn0~sPW)W~kuoxrL_UDKU&tM8wt!S3K`soFpYqPoHYDLnCOb8W*AsQWuij_uw<(qEvjNU>q?n-?-'
            '7Qv2+ceHdP0t4m9!S{S5{yRNYd(gw9-'
            'T;l1_Jl(1XspZ(h)|B@ek_FLf1+`3m_9pvfgGYU;MYl7T+QIrnkvOVW(B6_pnx;t?wj$4t3_($VHu_`Y7`4LSK-m'
            'F>lIalL!Yj3jrr?LuPov35v(x6q8i}QJ2-'
            'B|N*KwHuO_Q^;v&St6u1c)5A5EsG^4vVfb)7({06FToSvB{(D6XpXSsvocrP+-'
            'QYO1@$UVs?5(H1vCCFXZctw!`=~v_W{T1LQzPTdag_jkf54Qa|lDi{V3<CdS*LrXNItOt<+JMTcK{w;%R-'
            'N#jc~Mz&AoF^}NE@=R3U<K-8~CGJzTG`j5%J!}?4{d(r7vsWxrN|Oeo}K(xhJT02eN=69z-A5-'
            '%B7CM}DL>^8h^Ew0@5wx9OZiE;H>8y}~ob_|(Qr2ttcXr<EU7=o_b!djnAf=ENgM4T^7o!}Ib2vwAC*LpZjOHzfP'
            'D+$8^1pIb7W;pY{&-'
            '_|`)UOr54U9VXFIzAAsUeTY*HOO#6(FCZR`8m9qAF<@(_&ez=2_?4!=_#ZYRYx;ZyLvY0nGi?doqrgP%euXWeg9$'
            '!L_s!zj%I)8B+0_Uf*xbKPtUFYu7|j*$an%-'
            '%|YF%Hx;u6GpRs<Gw~W3XtF;vNkmb>gT6v772~9GuoGK0=tDMg3xcRNgm?<fZ|Jl0$l&W~A<oFgBg%<lAy!+!qRT'
            's=yRnZ+8i9u1^zkyY5$bG!P`+FN;;W}jZmszo+dN2vvuIYOY|FPzv-'
            '$Y8wJD4}z>TG_5(t>=f`~Qk?cJw^mNH0MU|SWFZlHzUqfuh`4g+8&4f&|Y`RFLB1?!Bk>t$%8&aDW<nVb9Gx35TB'
            'V?nHZHafu7$a9hu$rB3$IsX(C_cc7jjS#;38q!`PAM*SDrx^PoNX?`{7MWDz!tOxH;sZ2CAfh6R{iqX5?uz4UOpB'
            'U<<v6ooR<)Ga1RT*Nx%OU1dI1K}#8NRGhn`I8GW^83G=>N#HsIyFo333zP7w(S=TZ0l_HL4LW5&03?=vMD3<3#ty'
            'n(ai56MH{TG5B1_*6xll}lV0HImteBRdMi0+vQbWvD+E`@}%}HF9nIj^8@)dXPN48@J_p@I#&z!phz8(gps1A+-'
            'BT_=+i&8<SnESI7-ZCtT)w(8owAs|0$Z7ql4d$EM(<2C~f#-'
            'Vz|Omy`D;ASAi<>YE|eUp`e9;}s41s+Y|rOuMN{V2qV@CV5!^-'
            '<@1+ilzZ@H6?Srh@|8@QBD@#0tIe}$w@7Ze+$evYLl$X#Uk&2*A2C#UJ1~QQh|Ff(L5UcYh(}y#Vx6o-B~6?-'
            'BK?ppuUxNinsIDUC>*-nzJ*LadfYbIhud(17YXJ6*c-s?&qhzbSS+cPOv{B-'
            '<#NFyEV6lmkCu)E;=*XpBK}~22c}YoWjFto215HTnvcE=uST^G2*`~F^hj;1Ni4&UGHv_4$SIeK5tAu#Ipf+VQ3t'
            'fu)T%k40I%;cimRW2QeogdJJ5Q8b|R;FVIjg#buSq!eUFxz58bD-'
            '}A9iCZVxnJxqIt`5W>s^0$HKKiVc9x}u@;w`=P#Bt+i0P&5VhVX|Cd=`r}#?-URbt-'
            '0gv%q0Y+NFFD2n`6|@7||3tc_8CU=2&*73pkowK^NmSX}v<5Z!2Mv^<)Lood_C|22c1!Tg*9L4ue)O9tC|qtGe20'
            'u2HO!`VHCxVhc;YIG@BCrCy<R#d0f)aWJVeHcKttv`(Xpzj>~+@!-'
            'Jp^b*#_uf1C8tS;EEh%3mFUVc_j$yWr{PIC;i<ly+ot@@c-'
            '@pH7v>j{s=GN>Y;)5}S9L4nrLgF;IgUe0(*LjeE3shY{$cg&_pdDU)TE>D8T{@J**-'
            'Vf^B`$NwToD^4_e2r%X(q>FAq`=C@D`PeYI257nl|HRk<poCWVq!zo#5LVGq3_Fy=#v`I=@`d?MB88zoN7GZD&CE'
            '61p{K{Vx4Csk&}z;>fXU?Fp*`hsAT2s*0d2Ga4k0?9O;k;N)6&|DM2g{jDvlxD(ro9hh1RPIy6xZTgwnToSO~Z+g'
            'D2@K^(fxS;K(*FYDE0b>m(vM86$MC}87fEN(+^-'
            'Y0aoaRFmV28duN;y~dBGhEQLUfzroN~ll>jWcPM$UZBETdwNaW(tx3MWJpgnW+TCf#z}o^bs}z;|pMuidqv4iLr`'
            '__wSACH5oyfpd00sa~tQXk95-M%u2E)iupN8!ZZJ7KeGNF{(;_-'
            'qIesgVoU!(l|QO4f@^B}W#dvzA1!7gAE7#DLJXg&PCZ<CtZA?PFpXXPUgX{@q_d5=$b4!(;Zt3EQ+Li>ooCFU$#0'
            'FhF_H;x8*bBmn-wkaFMnIOmUz~z?Q1(1`Y!oqu5GPc()-'
            '&HruoOe*7a4s##{+&R>`5enaBegPK4tory&pR8hAlq`=V)Zj661K8BckGKLGJqXdlVvfHDR%Cs<QX9OEMK4#rr|4'
            '3M8ALtI^0{yH)F!IdpcxuZWCi4lA?s9QF+k6<mIY1e4VK1dEh`<!WUdgTY%Hg}HcNNze;qyp2Q6<4_DG<ay3gAaW'
            '$M8uEi@}lN0W+pdvZ5*d_Yq?R+bC>D2hs(C1FA`gIwpN6bD*)UY3%O%&DSDSzzztvq0gr<<=#g6yS#H(Gt{#p#48'
            'xFjjwz*WvHvacJ?Oy`7e)F?nwF56g{hU}d}&a;F#F=uIWNU|lp-RqU#}5si8**l?Q~|a0M`;)ZhK0mmcH?XOkX4i'
            'Pfxx+e1U?)quocpOMawig5=ToAs}&cS(3sJj{z4Cn2L-D;4-'
            'S~BtbR?lK~Lo!310p#JL%h&YC&d9pGe37*??*#BC4<VvObR--1mCl;O9yno!2*6$*u`VwKb&9yXi^7`Pf}VGN}NX'
            'z{QJ|Da}#aWyrC9aG{F+||5XHER|Dc39O$E<%Q4#H0<jsFxXYstizSa+-A_-'
            '10Q<prF7Bp*RBxkr87wsXWDU)pOt^U^oE)qA%z{Hr_6Go|nps@4bU`(Rip3j@1SUaajz5T$#z#u$lQ3oz{okVcS%'
            'IVm)v=s4*kP+fGy8y0?Mlm>LjAyxx@MO3am78SKN_NsI4s6$I|$rDDzC0!yjg%$v>C)kJDJ)#tr{A{3}#y~e0!QX'
            '5i{8;Xo~!rc`UldzdajX5^i8}_xzB(%jBuS-zvsXCFI5bF|9aSmMdyWKOS_RPXQYxC4#t<=8ul3VrfyRUCOaNU{u'
            'xH(q1l}j-'
            'hRTxD9#OY!2v(h09H_CnRUrrCbTeB~E@~B_#QcL|B#F81RP8ZFm!xEL+3LR&6=A5ZX%%XONE_&CO#o|ga?zp-Ja}'
            'H5`Ce5Q`GE*|Ix8iu&vdGLx+|8dUYF66AwSONv_St(O+Yd0o_^5J-'
            's<c#Pwmn}O%l97bo>}&H#zSTBe&poXrNN~+X`YV9<79Yi_1VFy>d95TDzY?lUEXvKJQ^s|Ihfk-'
            'nO+2eH)!)qk8SV7Nd%>BS@(er;vTnMlfvM-{mZ`X;xVAkyj_@g4=$+ZA-mN^Vl*hSn-Br&wT}~X<ws8&Y0WpBrIb'
            '<J-'
            'GIi9_Jt7Ewl3dvKMk)seQJ8Bvd8X!`_mf(z1{ovEVGDk`b#A`(9p_i<R$}IVgj(s^_6(E{aky(f0uH`N~Ylr^*x4'
            'f`q#YLT%8vyqGD1TqG!+)j(-'
            'bNzmXl5lz(J`8DkMttAqA~SudDKs;oLc>DnHFtTb<k*(Lt*dd0SQWfH#xUKW1aAn!x!YRY0o@Gw$;)Vyx`N`DMIC'
            '#f{~AJuuYd<^F-{^921oTuNN|KS!-YFsqa$x;U1*?~9N-'
            'FIJ~|6$*J+pIpVxqgHbat!`iX1EWwNA9qoJ4B@s<$5>#zEqMI0taP3M5fSA?~eJ@Hw|FMg42|I@$mfH;?ZvEG>||'
            'Q&4HsR7Bn-RD7S_MxN{NT*fQDq|9m)oIPE>z(aWC>o*zAx)3px$KY#!2x4ZrKA*IzR*PkiZH>PJ`DxP9y2gDfS>9'
            '?RPYqvUzTiNpgCgw?=a3kP({62RwE=lIr0o?wsS>G&*Kfw3%dUliC-'
            'U3ckYhY5YN|12inW&nb2Ge0b<{vOK{$BEL<8PPi#|c4XFZlw*--'
            'nNW`#8Bnr=ZJ+Y7}n#klF%Ma#2=$$u9igH_H#nu4ul**7C=P>WA;X77P3C@}YfUOj>{!1%4lVxBLU#D=7}{;q6JR'
            'PJvXP<iNz&R9sdVf^-ag6T~RKV+eWWfan|Gd4od=X383`5g&~qLw%prSLbELx@5EaRDU-'
            '{`0nc^f+8Wv?WYXX9gr>e5aN$hgpr?wtVxEOt4t2BzPh7{v%WPi!<{@<a}wBxOXIjtb{9ApfxQ`?ILrqqsWfW*)?'
            'Kg4b)iWeW+`P1Xs?3Q@&cL+uKyOE{Zl+`cA5m~^f52j<m&)jOu2(wrFYD>1*i=2$2TYCtoU8BVwGedX7{3KS`we7'
            '2kQh?uAJ&krdC$UTj6VkirHT`C2CzL)d=T@lm&dyxFgmve!YGIEPYa5QMT3BZ;I*q*(iB^0yG5wcOB~S{ic*1^c('
            'y73F4;q$9YW&{*Ax!n4eE>YSWF0KH^-'
            '~CsL%DUuN^45g*NOSVHotFgh#e9!iKyEwQG7>PB?PuQJIksfaBeB?5OcYj!Bl@XoY(&pI{f`Jh`<sWr@<Ya-Dd2u'
            'QaU{@-~W-'
            'xO4$3gbf_e!J`bDnT)P?f+{m|8X=MKQ92?R+**ywnurjLKj00L@~fVHolLaPpTQwf_7s;`r2gjvCO8(HY)S;uIpq'
            'WhXUzvRwy)E@;TB;@IP&Rz4(26UH~Z@@($V;Gq+bGvXnau0;$B#Tb^dYv{jWl6l76<fWL=won!rNd~#LS>&xTv!_'
            '{PYx`KBZxxf*zT$$}sh^)HuC{*0L?Z!*D+b`;*`;tD-IMJ%O#sdshsOe)+XD-%0L)5G*PMaB)E-'
            '!K?3<o+~moqZ#aGD9RSo%10!tYo}D$0w?wcDP*x*hm!bK9=;-'
            'JyIayW>ZXYz@YeH9VdDcE5GPA!>Y6!YlN9Km45+EQO955*`L{c9KWqUFgI6v0*4=pM9H-'
            'IpMtA2yyfWC1YBJAv@$zzbK<Yoko#*h-'
            '#p40~=eyZOC(;5Iy|6_sGYl3cvTQD<@h!+N$WK1~Z<;&xFI)vD(dn|J$r!G2G3?8#x$K?<|VoAIhuEl{bQUQwYJo'
            '4XiV#q@tLwC{&>wb7e=y|C$PtQG?(Xx<RB@8iv7F))E~eAn5Jny&JSHe_A7PT_BO<3o{ZIC)}E*7@G5qtl5J{JX='
            'k!pYX{xp<sN6?@+u3F-74!rP6};{=q`6aFZZ-14!ML9Yg{OC>U@y2z2|=q2%=-'
            'KTzf?BDfEnV}2k>YM`US1gprMBB@al8VVNF!|fQ$+L6oJu_<)hp1JoqM(m?VFV0P(lNx*EoPo8c5S)UQ!I{4m*(4'
            'Oz9P?O_TIS?35^5Vw(J9p;a=MP{y{fLkxNKf-7K>mpRLV-'
            's#rF0Er_V(i1lh{kx`>+>uB>OkUyOw!#Q1>HLcBr7^96E<XlXXS^(c7G&Jp@dyQlv!3>VLPkPNMMf@i@x)y5_zCj'
            '(UTQS2gH!`$?oPQD1veCnZSn=r7z?uK&YQ4c6fnt^nZ(T(9QZb+X1C4;d(1~!0&!l6<NX6=*W;ac!&Z+;prU2l#N'
            'IlZc-'
            '>OJD@LPXF!TTCwauP5l=yoz@EZ|sIkq8`Lc)T`OgtI0B4C%%&dv(<>f)~M%vS!?m1$rbvwioP=uZBRBs(VULD`TO'
            't@emno&H^2M0Gz-'
            '5o@$+cAvVu0pSxxma^mz@ocw#$72^<ayh%I=Lg>vH@bF{8`s1eQPPQZD2o(4rU(t>IxJDf_#^OlhZg+{W>QaPD*6'
            '0I7o<`1n^T7$CssV$dFXKQ2&;B-)N;K}JS9VII}WxmLACj5P6-Y}u250taQ@RYDsM4I*t>xS9bF>A=y!aTu-'
            'MAJH;hQs7zv&YKQEoN-c*;$(+S6O$5@UQoVUX*g_SdPoIJ!nN8$1g!3LZ(ctls=*qsTv%Jktx-_p${-'
            'Bs_myohzIO<ySTv!Z}P~(py?Y=kw~#jtQS>YjieSEo8GLvknv<TQ+pexJ3F#RI+8WT_N9{c;N`*dKc5_(<S!3i9L'
            '5LH-nTnD=y|oXu6KlkmVxzLlyN^LPB&k#Fp0LYb$jOjc=hT9rfog^U#EvJPfv8i%VM$IPv<48xNLV=jCH4|@`={4'
            'N;kRGsz@o1788KHtJq^h?2HeeKH?7f^p#3XG&e5n3Q10SbWznSrAq#KG1*{QA|rjYv~mlhrx?e!XsgBw5pnSRS4='
            'gg4B<neliq`eOx$Hh>rGV}(Z>?C<*a_A<a~@=>=G^X+Ged>xca$l&5qHlg3P|8SEhY2HZ2z$R{adEG?a2o{+S4r9'
            'hd9>9%QI_?#TkPy4<L6M3GzYF&yY*HN9l7M+EYuy0Bxw_(XuJ-'
            '>ffdEUH{gH*4XQ)!Z~={XrLnl|5MN4|n$+SCCa}h6^$)Xw7b?*K4d{vPOlYfDGCf=^rgkjj@e07|WlLgbXvU|A84'
            'kajVWbFi%mvFIP1^fr$_<XU3ey&vfpx$(<taj0w3&7Kbj2R6?>fUPL(Ue@vb<$}28x>ga}zZrqKTQyxniw?vx=6H'
            'qYh7xmr?OgAB_VK%ig{Cu<Xlu5{{xS~>ZrKY~x_|s;R=`z7EgBEJ^b2$U<y$RTA4$fiAu!y5|arKi`kk`Zn<13ej'
            'Ha=kCWbfk-'
            'f2u!tCZ6YLkvIN+!Oti(HBCIL`T|g;@rFF!G?#zctk>3RPVtWM?!sSjU&b##IqOmu3e)|Ak|1CNa_)SWX+UI%_5='
            '=^P)k}0k0dG&1)MU|PXMTGjv0{id<fV#cSx$DbDJequ~u#EG6Nz<&U~ycloeoVH^F;<!@BTj6GA|)F)oS&sY+RCp'
            'gp;nu@f-$Y#ExGN~iNn4x5U&72CW{Y^+vi(9R*4nN)d)IVG*dP8wX-nU_CFCX6IGDi36_urnR0c|m&m8CdrET3QR'
            '4iDFL&WnxyCll-'
            '6m{r_nD;n=hvTEoKWqh96V!`<Cc@;hln4A1<co&hhqzCp3Y{xXIg(Z9pp57z5ddA?Z}+!HU9`ZWIeAb(n*XaB3}2'
            '`1*2wlHg?1zk4O*XXOq*zY8#0@!b+GA$01ia=N>#~f1?vuhL_2*KF{QRiAQyfajF0wBNwUjw0`7K_K>9u(GhBI6%'
            'ml;Q(Y!*WeUt1o~FTuGB-'
            'V8BZdCKo7BqNiki{Wy6B%p_I4=k!Jxtzq$&k`)oRrI?LF!_uNmFHvsYc%HCEzF`r`6dLZO8DWonl4Q*Q3*q71;3{'
            '5;5MTqm^2r2VGPrp~mnbh3X&kNz=@QD{-'
            'i+IF4w{HS2rM)wL)*@(Q47Tc#>}DF*Fi&NAe+{U%@s11kAPKX(b*#LnV-9tJ-'
            'k&%cc=%VBCbtr{0W^eF&gL0=6&<~twjKY`Romiq*bHjw~@VOk-^B)2(rdsv8wLk2QmiGjSLt|-'
            'm+=~J$og)1^@oanQCM_D)4WO!|7QIGT1BP+X#pICy^^GpkZ>^nX%VNe0ft}H`~vQO6#p=B`x;}yugb>ed|5#;jCP'
            'ra&`7*=ucw&3}oDF+`5;VGWv=j|DlNf@$v!!)f#Eh-|$;-'
            '6QPCk*;@q!x{~kjC06x|9{KF$fA0KhM8#s!1mA8cLk87uG5xt}?>h`ex_mXXAweZ!IBHkB@@A>7nqZYn5EnB%G!X'
            '2ybo5FiO-'
            '`nhszQ#>3c(qVL+akMV3j#0Gb64PX`Ma6HgNPrx4GuK%X$xWC6!PQvb6&Tc3Li5TG|Lq!xDPRl~N(MK@8`aQF=mc'
            'o6}mEeWRB|q}+G{yM4l<|9Dzg6<Q<&BPnlkE>r^@?~)$dStY8cS2f|QAu)wkM!LCr16V~85V=w*d1#m(i=RV`Vuj'
            '^q!rflNPoXZT5Xn_y$#7qbK?)55OirY$WQIb$2)*;kViD>41b<Hs7K<=XOxpF1o^W}OpFWH3+jwzXc5b|2fq|?X7'
            '%giucsYMb#4W`(gTIlB*c;}y(r%;~Pl17b=V7yK)s8xm&Xsp*qX-lk!D`xyMv(!q0rKrVkSQ{PYSx8PUHx+m?m`#'
            'o-niwBI0zCy8%oA7UA#mL5&O=INgtq-'
            'F^t?|Ti$R3al;^^7Jc!?cq4pa<Hrj7P<;X=I}y`7LIJBXWi_j=WLRzs%aA4K&vJyiRx!p!-'
            'PS!kb1e<x1zH$;ddz~9%ErOFPMG)awHo{UTNlKnlI=jm{)~v7;K;0(-'
            'zQ7Vsw);dBDhYa0+ig#yOt8U3$1H<YMh+PO8`hUqtvyS@qri~R<0Oyl{uit;fzpd8z5^A`NB3_=uim6-'
            'P?#>uGWnl(v=d>)dB2Y5*-m?xvmN12xNe5a37nhsTc2AZWqy@I~1<2z{9e7^Nw<2v~CPJK=I_1p^7k}hh-FQWxO7'
            'd7NP4NX{zs1q=8H8Bh9RXYFn0vo{`2eB=DP?WYICyhpVb0YiO{M+%p@*nw_jy1y;X&7-'
            'L5Tdnx;bSY{Euu2pbZw9U5K8MAL_YAn~cLSTl%>W6Xu{(MnS-<^~f6-'
            'csyby&iKko<?cS+CKI)EEK1dcNY3Yz;p^MQECbUdItqY7S&dy4)Fz9Bg4Tfu+-'
            'a3j?Fdn!O~{NRDoeWi(^ArIMwBS}VW1bdDbSt{HmLNH;+d!%K_0Yq-PwX)=9><xs1cc1W83Tk*T;?_Gx^idl{Mb@'
            'Ul_KA+BJkNjb`A7}pi>2K4xy3G_(4GFc!nQ#-XqpVU-z=670*?PB>F)CI(N-'
            'Jljt!2Nvtd#{b!<g$6MwLy*_wgfb)2QnqcC16NI`!{paU+rFe7igf_tuW7lrwrhk?jEUfKj(t8OH5yu%|DM_#Sft'
            '?Iu82g4Z2w1)*dcX+Pag)KyZ~Tr(^Y9HMlNJkcB-ljOvdnX8N?+xHlF!TXHE&D$3qy2b_lC*--'
            'x(ea*M5m3WKsvcnOk%Vp!Glk%AJwYE$__#d)!gMT76TR(4&y7MT?F@={CPsuoai4?j#K^fwaN?IMbdzu1eJaEXKV'
            'N;{hmISM<Vw4Cab}>_Br3MonU#FXu)p8xzOH#%rYuGi?S4S9iVT?d`kS5pV7ZjGK6OU7EL0&<zXSGr=nTWmnK2kK'
            'X%Ws#hFZhkHdi9H-pVeGAeWyjhf#B_oy?!`P=O*J-'
            'q<Jy^5?g^XNs>0D)M7XXp0q+NmjT%i~*1{zl1VnTp4*OR*X9xGWOi<-&)q5yR@ghr(F^W(-*kRm-'
            'RK8LqxSC6U}T7YJRzayz=szyI-o1ANCU-fIJ2EsQOaChbGonmczXjD0KI=HTPqQ4_}j?KPFBSAA$ouNFuKEovHVt'
            'Miz&W8bw>1=H+du;5^K*wFNzCe@#z0f`tO!7b5FaQDL}CRe1`IuCULbt{ly;!bED3rewE6Paf$A$d-'
            'I(g3aa7wMglUjW%VIBBV>^r|3MownR!R>9sn$`Xc8HoPs0-'
            'l4vWz6Myld)E(zCW{6>XyYioZh*ZsTsB;guHC$46N_!ix4DYlsQxY6Q{%2FMKX87If&~9%KC(D^{2FyjJGSS5;h2'
            'l=E0bzk#Dclv*Q#gPOlxNCd^x_Jtk7iKz9}COeYLSlEx=Gq<fU?pw5J^dotipcr4^TPBf{va%Ew6muC#T~d8$?;b'
            'fZSXI(g=Mzf|F>)ZJ&GS*E@~YOYI=Yn(ufMr{if-'
            'D=5QdvgFB*<HAPX}`TiudMt}E;4|J+&)_Z>>@WH?n1i7bF+oVYNzLF$gk98m46g~jv_w%*95bnDhi{Ll2{aonNtx'
            'iwa-qDq6P=cm+M-'
            'og@%z8k(>O;cXS`A;(snv7lvc66vh@ZmMX`;<35jMTD?=MtO334>T}?!V9k}4e0gY**d%NMzK@TyU~Ua<rs=sSBf'
            '5qHys`NV9Wbe8+LW^5`SKs-!96I<oSYN<G*Gva-'
            '`x`iGLeCsF|CEV%u`;?{;h?SZ@;wG`sLYgR(HMiEP|4FFZ&j+m_8e`EQ+%9%H6jRyzoI0U1&Kd6~*I1^;UGbOSAs'
            'Wju)BP;k@q}8XPaAkiEebX-'
            '7#eKe4hveytZXvl0GjH0WoH&@8MamfOpgq_HgoVk^yoV9O&=bS*#FdMA14t_nH$Pr4$H-'
            '``?=5B&96meSVf5$7Z@EywOCw(_iX9)s)chE2yrQ9D8}+uyxZ>HNgS73w|o;3k(`R-'
            'E<~^Op>^<B+wM+Y@2at{#2$;s(bYDMqU`;t4U>6soBT7IHQ)+X13astBfTVZd%zAocTs-_hk-'
            '0ok$S3w_EY$^T&T1xseJvU{VwodW*+6yNs-'
            '@u!f2KTgo?C**D=;Aa1lD?Y1S;Z598vTge#k6Uu}r3(LMtDdYe^+E3UMyD8O9zK8$M98_AZ+`@gB45Wut*f>%?PI'
            'v--nyR_lB&7xg%gz4`mXgdaK=?IQQFuqur+9;@C}c~W_Gr<LiTmf=p^QI%y5_sUo8~c*}zACV);DMF}vhCuj%ZY`'
            '`+Js-mkwg?&0}}qz#Xm{E2NR*Tss>0rL$AR!lmgu`+!sz5#0@NG}@RWaNH?!Fpdd<vHpju%3t1O8yCLz35W+3=fq'
            '3I8m*`f2s(OG_piPkyo!Tk@=H_UfWcaG0An%sx)wP1%iudzaX)73*LwF5OiK4h8Ue>Y`pdpZV~i*u~QM~d}7FK36'
            ';n4sDndMG%+I)J^mKGF#1X+VS>5q4H|OyI5@0O3~^0eF7B16;$Hi=_5(I%oupd>>@HkDR|%O?UDqa525Dj+U7+s)'
            '`jOO$6)DDphssMUVmzhH0Ye(olc<$na<|mJ+Ehk!PWuoUOod@|jLLF6CbAhNTCN9)OyuL%$vZGk5j|h<3#En`^rO'
            'h+E|WwP<|mxlKR}~IIwmi7F^Y@mC}7o$7<0{t!1S0{47)VR@T)O~-'
            'lU`M%$OEr_Igo>*<6+|#VQ9wYlLiEd|1Mb!1`jtj1!%D>21+PObjw^HuHJ;VLSz~W?nC5!wd_0r?~ty;E1EARs+!'
            'S^C&~^mvthP?Cc^{JjUlA3b_o@x(#~y{`vnxuuqC$27nopqKFo5&Gc3F;UXekIQKVJIeNt;E$w5V)MN-Hyk?(O-'
            'RP>kx)ffml^Bg$hL#6QXrKpJH0_tl&Mktbdr~l>bIyImI!@&}D_4aqVN8BE8m>+Q0}s1ZXLi@|)jRk%=F334<vuA'
            'VxN=KgzuOOlh5X&5ZxMKBI%!hoSGAQip4osImirzD<s8K<2kh*;A1KwdCm3g{iXpw_8GG&=oxVzoD$_FsDg$9!hc'
            'gH4_#+SmK0m4<0IhZdjq*95$!3MRlQeahf6h2YG1gZ0v0*p`58C8Vj^lypudXn@NCt-'
            'V2@2SYz%PN!&v^AbB9e`IJf&H1ziwu#)O%++R59)9-jZI*_%lAri?YHp1y46CCU?8O2eUXsQB`GV;Mhn&II|-'
            '$d_V>D<!Tu~q4+F{*)Wpg;vBBpyKsn#sM(;e!&_s8X8~bcZ=S;J;@<Idg>ga#_3{P#A)_%FdU$Js(e{7!;dPfG&h'
            '}C*=-p6#s-Zc}C-5jib60N3#sKdXNS~YYFwj=%+y6Y+`H#uYUw3zYKhAf~9-'
            'yCco=RM?1#N$eq6AtBT~jW?D3qF!cSA5w?gRC85<62qME5NBc7Hp&GdCJL$Xg#GcLpCbURD=<4le2jxuqfLpVVve'
            '{>G(GXkcnz-aQOW_ck{5bztl^MxBGqv0?{C<j^{u7lor66S#mSYfHd=teLAnGPaw$x=dc}X0LmjzIvH0w>5#?%MA'
            '80rm%Y$Up<qUI?Q|6O8%xM?kx;f_cC0iJ%+h|Xr0m@tuJeQnZ@6hk~Uwq`ImnNK--'
            'UV-^19_k=~Om+Rp1Z%)gC3?x04ttG5)0*u>B_oU~6l#M>|{ZGi&(ZrI?+wqT-za@>P`C$na!9qUl;KE^8t?o5owv'
            'fu(wl7;1Hq}JHg)9R!}Tv?(%IJGbM#<7YvxX&qiqK(M=c)$In5$>z|!;Yu=#PvywnXbCt{C4Uker$R9``r5dE&{-'
            'c5M3>N-#m5ZK+?XX!z~vkN}KkSFMSy*ER^-'
            'Cyd=k>gfpKwbBd{g{bWg0>_J^P+GHi9OuwoDD|2{7);E@ZaM(h%U8Rw$HPSrZOw1rAaJ7ui-'
            '&qe@z+C`8;%^4(a53)_H5F!Wx$wutTGMJ=ZC}ha0Tr+UPLW$hPMbkM#v?L;9&Dy4y0bA}JwCW_Hkq);L{e7xt~ik'
            'DMK(W$w$#&W@j?^CsOSy1v93eajW!~xwIwT|h!`$T@})}bUTvC~G?Y>#E9M1<F6F$GsmyjvppJ36G_n?rRQGq=MU'
            'rLdVk4LBzE`2ICu>L1`IrGKuIjeUe4Pc?nwEODZBfr=?b-db#crAYgSk|-'
            '85A%xY0QI4@QR3+Ph_3BzPJCrhKFf=wOkYgl(0+R6LAYkv1y)acIWJiuH~@FV(c<(FrpmwRQ^Jv&}5NII!8k?!a*'
            'V{0Zo(m5QxGfJ@_=nx^6>VyP3N$YtwODgnsBeFNiXiEac%HW0fsfOgUMY#p4Lzt+Y_j*@0udEv^y&1dC^-'
            '1&SvifZcjgqgMAQ+iN3a9v9L5pTSD*nOJ>D+{@_d_$PE%x%GbW@XuYVG34GBs_u_8{N6)ruvO@Nd)U2Cw*?mVGXi'
            '%Rg5v^zh%W!r7;z&+=z9(yh2t1;jvxA$ZRicvMhu$Cwn2D>^u`i6tFBl@|7o*NU}KJQI3H<Pb}AlGHk^M1+cJ_#;'
            '8Io?L~GVf`D_;BZLGfrMz~JMZt9|Yn`=E${$5sE8GSud9#)Z*Hi}-<*RhhkA{hYD-`F+M??i-'
            'IcO&YVeD~oxBQx#|;tC|SX)7aZSfkK1#cCZ$?lp*N@62oj+%HCO)G5SGwPOC3_p^s?EokmmhHZhPWY7*<qdOnwPi'
            'I}&-oSh>YeQeFL$}p;JB|33_S>+gToD!2b*DWB*is+fZ{zpKW3;6i#xuvLjfc%B>&sQWxwz~F5@}JP$c#S-'
            '=c(j~I5FV;ui!=Rvaa;QjsDh__J=60LcS+teW)syMbITYR93q^?wPkK4Z%_6f&yW;eizkgwu5pzFvdaH+p@E*b;q'
            '&r@RQO`RM^(TZ$@iFY48#M+unFflS<Y@koY9_k)Up)r%~je+a_YNCt=nktl<5ZE#+UfluuwwVMzU5%_w9qiJZ{C%'
            'qai7W|VuILH>VBx)cx9kA6k&ga*jxqF-AZfc{1#%hQo6fcCU(-'
            'Rgt7ztw6R^z4tCABUD9<$n|%@B50jquUm!CeW<iWY%W1`Y6L;e`}%C$B7_%&PcYUUC=_gzpWjPl+ORqW;mU^(=)o'
            'orgUs<qC|OKi|XdN%2D5%=}yH($P(wh*lxQ^$WeKVc#EjM>|fcu{yDOF#cg>iumWkRSVSbWf{_W00&On7IF7_{Gh'
            ';=+0E>^db9U|b=Yuydk6wPiXQ<vp-tZOxwC&deP7nYcS+IKq3%mK5B{k87E@ZOh9FXGPnVLUGa^^l6RGh5MTjdf;'
            '-$*j2;LZ}G*yfHd&?L7>JWPaX)n{fWEEWcxXnfp#k`>=u@Q_*h0{AR2Lj%L#zD7sqjUq)A9i;F9De&KW$w76~mPM'
            'xRX>+!S<Bca%+@bUm7P*SaR4X6ZqpDdFcZH1xoQH-'
            '=S(0A_R<|l;i)LtqEQOYurV>Ngz|Cc>5rp+BQNu_wHzkRJtl>$8)K6TIF$}}&RZEzWtsl*B=y;%!^P+%5N6A&MYn'
            '0?iFHepSpPasWlfOCq{^;cN&7bpw)6+LcfBNzCaFo0~V?gnLbNDe&LovqAl==)jVj-'
            'J)O2?kq)q+_9a(X$2m?*($q814Y#v|$y3URQ_Wqpl=03PYaKTM3;!aYY$_TQ1+MVhM*a<V9?Zm?4JF98o>!B|4ae'
            'AJWr9La+|*i~@>%}73?1HI=tX4YU*JI}k|-<o?2EXNa<hB-<S!g%E2SNUXhvAIIn#xAUI!txOIW0BS-Wx!eTk`Qy'
            'nlzX9SU1Q#W1sY9PwqK4IRzirg0L|d)uj(748n^|v%xsI8IJCa3CM6IZ`x|iyK<e2SMBy=N9foiO@As0E;@3?9+~'
            'Ql9`phni<D7~*GWZ#(CQPP2(O^9DuWR(sTbEZj3=1AWY~iihK!;xq7>SkUbc=K7W|UhS>QO|iI7!t_$HwRavR{bz'
            'wZ5(zlW!95Em2wg{LRi&W}sk|v*i4SD=Dg3#sk&>aA|5}2Y7fn%szi)co)a~m7yk7f(W$fWsRGVpN5LJQE(i~-'
            '_+&9-'
            'C}2@TGZaCC*s$EGK4kk0DxSTX0{q}!YI0N2Ob=Cl;oFj4MaA#tB^HPN~e|{>xI3l$r5mI9pLKpzGx_M5`fb4@&Xl'
            'L%7u*tf3c=<wYfSkR<GvAa=arU$B0E>5j=N@-'
            '$d#t1voJMNF3j+FYAio)F5qz<<2%!FOQ(Bu8@j~QF48WDZ3f5n1^bTTX%7HV`n^g*$KlC-MB8jV#r0EsLFmF3??j'
            '-=w|I}p1uNl9e&*CT~^3<YiXu|!P_$y7vCs-'
            '=R>?>JkcB)s%%n&53pW$K~xn1P|K1pz`$eEM}rXCZ|9i`#*>GN;QD1<?19vMbC~&2;Eiw|{V=(aPk%ND@h>erP+#'
            'FFE(c{kEIVbL7CC1WhfX_#CU+8L)CO@8*XD}YVupG9Yrt<sqXSYxNMERkl;yI*W<#ZzqQFeO+^7<f9#wcXf%@b`8'
            'S@-9&1s(F8=B`LT^v2A+2H>JRg^qB'
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
