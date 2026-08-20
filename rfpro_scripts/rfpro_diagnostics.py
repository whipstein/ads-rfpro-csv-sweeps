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
        '17d1c14d82162d600ee6bc3b7ce3b22c9a9170071b7c93bdcb1c6b1c50ddffd9',
        (
            'c-'
            'rl~>w4QpmMHpPPk~0xw?o7fEjyjev>c_k+LjZ4<BM!5$?kD9Xov(Qj7fqaNXu%CzHdLod4}^~`$^8a)cpd0vfVv>'
            'PN(}zM4+lrwQAL>bzf<kK3lBIRWV*y@5|YBvRsw#tMV$jDC>E-UR@`}Vv;n)`*M=JD4Was$MtI6B+XS>E|XQ+Y-'
            'aGQS|o3t9<S=r&d!_7B3WNn&|<u*mTP#`RFe`Ol}WuUMLYON{h#G{JxZRflk&q7KG9H<rkug!a<Wq_irIBjHD5N#'
            'qQIFYfBDO@SQRj(a&=Pvwka3mviZwjhDotp&Z@FW>P49>>uRx13iyAruIBL78b{sXwaJeTX+^7Y3bVh2jx;0qj#@'
            'A-'
            'f0R6}S4mUPaNXm2F{##7y?~XjcgDpcDP~Qb%<5u7W5EglC~6=NSPUjH?#nu9s`+MC(11I|s!YbKvVcVo6Ij*;|2q'
            'LN&;yu54J%k(RZW@9>q#}O$_YUE6v4TwE-C<%T-UCGPcp4n_=P6H(c$asdIdAOx-'
            '1t2W!RG?bf{N5<5}I5%_za~#D>AQt8>7IH6p{L1^_MUHLZ#I%AMOu({yKNx~k_%o=-'
            'RH&8p1vq?!{XiUsr$3*3><Ru?eArj)-'
            'g*YlbDyMjrt>w4D62lHZmDgUn3)0OJnY|ddKfC1`VbFKcwt>>9dighstIKUd^)YKzxv4ju7dga?={4Tv%UoWf0g?'
            'xUvxE=zo0$9#x<uG{xNC$6+iNwU6ot-a|BR~?yeS)+^2Rsoc4BK%%pCiJI2|)1i2Dj*9GcOnGX0-'
            'F<=;`54&rkEimxs^)eDdrhe|h-'
            'gC^<*~((={6zk2l|KYf)S{jbxbm!~K2@+shA315G?nZvdv^)#6PUI5k=Q$z*avq?Fw=7=bCJODY8<0nrId@p93k`'
            'D1^t|#&4==jx})BO1G4NT(n=uQ6Q=<%}`htKol=ZBAv@XKHC<j-'
            'E793MSCef0*K|M2YO^v$31!_(6@&;In&DNQ_IO<|vMq87RQV6O15Nq6!WM<+k#KOVk(^8BcMkU1Qvd{Q;bS#h0T0'
            'vKl{^xxU}pK417uycPc7YC=SO_}Y`qvQlX{WGp`e<y)|0Bv6Zr6_UHc<3Z~VS+}WpfimS+%)BCcUp`Q5mqG-'
            '#s>C@(0WAJkK?IBmoMPI`$@B2(Q_JU9}$Osih1+<UUNRi&9diAgc7E#4>};!d9|P^C4{y}1?7qaZW?pNAp!c6^20'
            'uC_nIEcX6|!iX!jK(%zm=oENA6g4dG!j8ja36m-l)NM*<J2Ufns;l!gF5sfvq5-'
            'K?u|le{b8&=fOV4Pq_gGE8fU#8F%%aHp)C9ia<hOb<2um)Cd=<<n{gn?k3Yp3XKvLXD@%e*t}7l<qkBRng>vO7AD'
            '<K&hxjxp-f#>II%&Y9T4DXwn6TAH;chQzDHyE-'
            'q{oC5+tVGrOWDu<;ifJL@G*4URQmKY$ku5;*D??xyb>I3>5R67w|I3}>vtc_=id!E&UMK7hu>lE{9!TGcD+!nBI8'
            '3eL%<$!EoRIWt~$fdns2x-'
            ';L<m1)C+u2o*6xKSl2;B<}a_vOmIcJWIZ4*Jr~apiJ>#^ZXkUT)R~&d6h?P@Vq`U5D8JOyIi!+-'
            '3d_&IvEp2I*x4!#0cJeNoNuP66C08bsLbLG^6$9uTlzT`Opv6jR_9_>M}>%QbBM0-'
            '2a;b+JJhF|8xSXbkqw1Z`uSC&7w&@DVNZ^Xpt7nF%F$Fm(6Rf>_lwFuz<8rE08c3U&6H5-5AL-'
            'z<QC7+;o?oTmsIu3FOOsg?$@@f&c9aw-;@0}0}<4}eXb4n1<3CA;6dD;C?$TZ8`~9fRwCQo-'
            'g5nmd%}3^y>2Jn{gmdef1dx&tH!2i9b)=DbsIP#5AeJI+%=N3~WHBWV`2SXx@o-Q9OTKs^T5qz1-'
            'x<?=JD1;Q!NC<-'
            'GNMEriFPG3?nBa5pQ0)TFS2iI(%2Fv;%!zX;h|4599ceAZ8K`NPV8enHPYr4=Rdnj&eOI&~zugaA^f+#uU@*L^|$'
            'ZQo%8jb>TMtDw)+XuH3c5z+66&GNh2Ep5MNKd)Neq?pS9l{5V*f7z5Ly}U+)yO3PN-gov#rRs><G7prXbtiOaH~w'
            'ei&=f4*UOUzl5~*Fs%EWm=K@}=*Q<ds>tWKtLJpI+XN+6?Z$J**=VEa^Q0E9YpVw?3P((L5nao0LdNhK0z*+{}RU'
            '>e7r)jDW>Ajo5tx$g2%@Y(Uw1;o_d$5h6{i_$SVJuYeO|e;^1l-'
            'UL;uQ7%0f+@O0j@UvW18^!ci9;Htr}SEYnU9HyS)=4w~|Ki;;6~l&L`Y(;N(dCk^i>NVaL`e$LGwX4rsgJa@v;=2'
            '8nkh8;yY9f{nha)|Z2HRxLIk(#)g7@Z$Wp599MuQ>URp@ES?4s>Rn2Q@`(T@M2P5HKWOF7VkYNR?sdDe|lVx>tZy'
            'yhQE1)Re@>^Aq*TL7de=wKP{TgQZTfyf#ns$?<Y6r*KSh<v{^mIn=k+}kLf2E;vWj-51V)R6}oMxQ?jb-bu&a+18'
            '<sQHNGUdL+FqWpPbx3dO>^=w$mt2(%13z34HL|(d+eNkOQRh;5Gg@G%@4#^Xhz6tgfFeruB{~iJ%M#7~75rf^%7s'
            '2wfo)gvaMCuImiZ-QZk`$t0I8uLqiqcg{Zkvz82`-'
            'a4WFIv_2{h{aEoi3iz8yc}qnSAH0ywD#(RHqsqR9eRB|^Wb=#0P5y)tggljNo{4{%wDGeA?{22N`0VY=G17hv=P4'
            'pjF!-'
            'EQhQ$hAjy5RwU`|3AI_^GAqrq=?)?a#4Xh{PZ=Cw*n0p?p8N%$G0qs?pAi!P&r*$S~h3G!x5An2M2V5*2&Gbx~fk'
            '91R5@uf?EZ!{4=5h++Y+@rsFnv-'
            '1CUE;OKj#41=t8ijg{3asJ3GE!r)~WegiP_C@ByGSNME1kua6H=3wHYS)teXa$4@^zdzl{}p8l8)6MStx$!yLahF'
            'V?YICV1;!;j#$8@Qi>fzoUQw|2E2KvM)<Q!X=45TNmVem}Si)YilR1)%5wH1s2|NxJ=glU`Y8M|T*3#EAbLWFcB$'
            'wiGieX0!8R{ElYaARRNdZAfQ%KsUguoK_z)zIV$H<#@A3aRoZ4Ci<yMsBqZ@S`J_txN6-'
            '}pj~6(xok@0U^J_*koM6<N7`zKB-ksE)Jl!PAF!pIa}fLAG1ImzVWv~WT3CvM9_f$AM@J{Gp5{-Uy-'
            '5`*FuE967Muiu#%Q1MAmtnttCuxhI_@{&ntSu=$5$_o^cQveULVxWCED?Yih?;d_Af5EM|4zSf9%0~Tvn2x;D0{m'
            '#v0ealq@zDa^qEHeFsq-fC(spQ?_PME!?%X4{tYiZ#sIK#aE9YBb5hpu;vt37qj|&U>w)XCl|0b>K!|>&e5f|+d+'
            '}_g_q^{9dqQs$I3g?oEr0C;zBYg(wW&GwsnobnWpf5vuc1X1LhDHdz)IwW5ZOiO~`W3ki4Y7E`S3Z{bvm<l^8iAW'
            '?#&*oB?l|4i+`*N+mDIV@3H_eJoOgd6m57jj`C@t!|U6g5`;6y;)3>VzaIRws8N>X4j)%7pXCr;4ERG##MRy>*7S'
            'LaUWN6BUX27_D#|L#J0WWzR-'
            '6ew>(;2CnzrvcUyh{{#NRb(Hsm^c8wZ{9jOH&R+}J!%r=P_ip_Sl=nl^%j?T97%8rNXLIreSnEytr&B9hKy-jD6N'
            'lFS@b7tAu&_+$%<^wXGIWL4(o3)*!>#-'
            'ZG0soxGf|^<<A%VRu?IRJCcOKW9nPh{>EXGogg)g+(u=g|`h(0WB&@Z9zG?;ZQ?gC&-'
            'fHZ8qLG_sTTQD~xlwi$z0?SSACHglEE*KDO+zc!hIaNrT;xO345Qd?Fo{(OB_~_}DSsR>ea+kiAXU2liFgf2KiT-'
            'U<p_-f7PV@~xGq_M9+Xp4JG<}HUY~{)8RlX`Wcu)+Ho@H>~eDwxf^6A;FuNEY@lI@-'
            'c6Q@tT;$v69<9b=5B9bYcmL)BumzHTJ04Aax(SOkN*9+Aw5K4jqBwC{1xfED|#3rsA2TyT!tz12l)Y%ePF0Bi-LF'
            'XIPk4#|F>r0rPK~aYEsT-'
            'S115!9LcEZH&kZk=+H30@iS@d5ULd%Y8?2~Mv?48roJa_p4W0z4zGvy#SmTP3<28s<b8yi|<PwSyD#nuZM(;Kobj'
            '*a-kgcZv>KI`32$-'
            'xusrqbEY_Btf#nUiaMkH;}OqEX6Hj9{D9NS8$;m6<RG>Z%9sKu?~Xz#xB4iLr8D{&M)|=Z7z!<f>8TGHK=)$h_sv'
            'U1%L{(t0`t3@^(CPIg``&`%=0b$H8;vqb0VWu1r#;hdd0B9<t_3Q^#TRk6Ipn_f6hImd~Hd|qr8z;O`v7e<c;?ma'
            '-HNA>}go;oo4xJ=Z#&}*n1*`tg7e-'
            'Fe_h)%6iEj32_c2nZztGZcYEF&%Yj@6sS#|_zu_e#HfD_@`h;9S|3#AMOL_-'
            'P$TE$|dwqh{BZI49O%?`~u+YAGnys=o~z67z=|u=qPR@@QEv6$tpuXVTIkoU;xRjZ`t%k)6+&m)sMYirN-'
            '|+s@V~t$1I;WNZWzrlFdwyepMu82Q;|AY8-95<xd5Nq1-{-'
            '#0%_%)e&$rDjDsmhqrvGvYzBGx0Il(225vS>GBa%Jqgm3y=7NGy*_2JWtCSL~mNJ&-'
            '7Glfh{LSl5z^TC19XL&0Y)5G&zez;flpBIp5XaCWo2`v6-'
            'faVnxY~6eZO8FFyd(N6DcgH*!k*0UC2JLAuAB7)>Q}2!*S)aW?6#w`*jr<?U76;H;FRBL+X%?;LgSY^NO(=?S2H*'
            'j<h!$fiklcjdNs0V4tgCH0IiYZRFxxQFZ}oC~;JJ`M}*ac~(1*uD#aEqEf_31z)lsAmh1b)JwFRw`=v${Yg9BbP}'
            'O%4~*|>DjuR>pfwsq82;pjF8)r@^ng`NzcF3Xep6--*`yt)<5_3pN7b0+jGS{+YhliIJ`i-'
            'Ku`!DBZD^smQ|kHb`T>4lMu>G>3CD-C>{>9_n&RHBVmC?F3?2^F;X%rD5othgoZL<8&mlKoeuG`M|@ap=H;pyv-_'
            'Q4d17Z@*dJ*(eb3H#sd$sh8%LQlXLJ|_;(gYtSEJeDf<@~==4sHBAY%8$W4PlCLQ~WBPU(dyJVe>Ca6mttYXp9XY'
            'ecxK>g7^%Sg!KdB8t(t%a(4gA%<PMg9=+TH?}xS)g}lb^_DjU=9Wh%3crur=c=|yk7MkTIk1G8HPxz7LJPkplnpE'
            '5-'
            '*StyE?6K2O6F=yh?rlK*SYd%i0u5(7+twp6BdM63pfnNt8!Yd67terp(aE*!7IP_bMzX6GlmY6=n@Xk=IDesKd&w'
            '}z*Ehx^{M)-8|WP~0Stn9a8uh)n%Uj*U$SvQH4CAGxTh7=-MiXF8#S1LIkReN%q4iztm$e96QZf-'
            'S!iZ%FPfk|<@jtp;>^q^`+JkJ*&h6CXPe$?1`@m3@{nuiaOq`@?sV%lAYtRsH|?LRQTm8RfzeC2IvuZWRI1b*k)g'
            'c7g-0jfyjRt1maH}l%PWWUJScI?S&Vd04Nl-_fk<n)It4CKh5PJ*MsX74giD>3tG2u$73VXO)>WS9zPEDQ2xNPv5'
            '6z_~C0&L9^3X~otWEU=Q5o185b-'
            'H4MSR@w`Bc};P*ayPV@k{xm8`vo{_tUHgMuqaX|{%yU2Mq+!IQC3Q}}r_lBVd%za*Z`L4PTs1n}Esk*BF#esW_25'
            'cu2&x2PLI{$jJh@r+Oc$@sW(3N1k`y8HV<!%^3yR^_rR0CP1eOSxv`%PjUh_2fpyWWs`n)xf;YS{aTY)FW5iCtLb'
            '3u;w9c5*wa2C`xvKz@+{y*Q#-'
            '&Iv{k<hBQA8*cCx_8|qI<gRW`c@s3!FEs#wxHT!VWadVF&@c^MSD3u1`i4nqf%!I!ySLs3bZEzz6Fa&R{zW0{)@+'
            '=E)K6x1s@zQsNqFj;f(1sL8U#I*P-'
            'N>Aw6$fN}Lq*n&KzNyK#_PdXV)>bKTdJ!#;I57T=rEsw9rJWx0Or63&w==_zd*f-b`PArv6!7W*7F?_-'
            '9&w>gwLhnTYi8{1P_-DgN^Njd*ED5!7kn=9r)W8?8y6YAo%u<qn}wfySP?6wOHQ8Y^ku8_U$eKZ41WyP;fiYZn@5'
            'FtY`-El9yqV=0)G49&E@0HMn6Z*B(?y1(3#&*&T}$qh})q-mR1~n?<o~E^Bj&QaA`G63r>&>}al&YP?o-'
            'NlaMB2a&#*by)f#+m)2&=>X_|Sn;WPNR{WUfQQiINcPy!O$lQrvJea|<Umvhn6dt_5=o>1bf@11ma^)`SfpV^Wqp'
            '$27puUSTIw{>Jaa7NVykahV`czA>KJ?|sm0w&<@0hmlh@o*pL2UZ&kMlyYEi2F-gkC#7>JJxImV-'
            '!9Yi`tbrUGSgv*Zzr(v2H1!5W}J`gb4f;E~tO63kfz+1}*i2K}f%`_kh6Mkv{Q;nqk;0zAIJvm(?8eN?eIy8qJS='
            't_9J?K7!otqZiARL=8Qpx?olVg&cms4`b)_D#Te@^O1Yk%$xdv7aS_CV-BSf<l~(VHdNZH1m9U{PWIh@hnD5U(GN'
            '*|h$3vAQUAIOy@?67ZHsX5T6Sj`3x&xDYBwUXy|W#&rPy)KnLX+`?C>2ys^p2R_G6uL>m_Hcx>>JfSg80LVf?;_G'
            'ddrX>8)Yzv=;sD;Kbj-cj;z;yWJBzd^^@Y{qxxr><KSV*)+kst#9=~(0-'
            '8(AJD1k2(YeQPxAG|2dsr8*KAA+}3*;-'
            '&~@e#PI^^KkV~7G$kKKMJ5?F(G&=v}1%**##Vs@+1I~;dKl|Y6Tr+YlGCdJ;L}hv_YtBIGYvPl6~Tnv);W4-'
            '5w4{<M0JL4r5?xBj1$8#HL0R0Z2-j^O98K04lgVWEh};tN@Rv-Ophjm-WO)qmjAvn8x4227AQMa=z4lK1W-'
            'mG937agO_U&c%f3cxwWXV#VEPT2yFo|>=a^s%u0AJBBD`;<#j5oSiX!d^(f_hxxSX8nK~4)vbWeC*CU#kJ0ce!XU'
            'NjSb%G&zYhovOF6v<ENmY$<dUM!x@rfAAl&@=b`FvXTDa0>hWO}(a6ZN2P&gOhxt;uUlAC=l<En_F6*ZD`4NY7g~'
            'YZ=w>60><uMa(@=3D9IFp5tt~DN%e(>yF?Q3oxX$;DPv*&1eg<+obz)DnKl(aZ<8e53Fa|Z71uNqni7pP^cAOBwr'
            '^-F)|xb2=_&~AUy}-OSKXhvnw!0PV4WAGTmHnbf5phkwyWJ{1L15b&Q=gl8|_}C?^m=E63)1R*hAzD>Hc!4KAI-'
            '$=IiaU(=o^I%uIwK4O~O@H~whR=$T-SIy7(vh`k-'
            'Blv;0yfSf@xOb((Qt^#JhIbvg_KEm!acx>gLpfJ6=EyHg(|jNQV4j)qJDsLKc<>|#`D6-!L<_8RJvWT$)x;Z)-'
            'Nf`@um);4QgQv5<izJ?3`ld6UoNkoE#8MfuE1@L)$YQ84Fz*x_2R%CinMc_<a<ES8rpQ@ug_7H2AgQ0Cg*msfN1*'
            '*s*!|8p}jxiElyS@X<1UL2=Nh(-RQlGw673-5b}bAQ@%S*(lDolh|rqXlg+FY1pBXbJx9KPqHIuqN5@m-'
            '8S^FYlgs)_5aVTmm%3zV#qDip)zexKK7%w17~Gu4=wefixc4!)`WdI1dHqHWd|Tq0(Z(B0#EKkYo*YS+EjVbRzyn'
            '|SgIeuJOb@sHCZMkiT_fj#IX*TsS9V$-'
            'aR(DeyFMvJA2=}>&p^r;!!rrf3{DHovV^~c=YZ|HCIy+Y!X$)%RIk^&&H8#)CgKR2&PrD+)WxF*1}5cNUt5M}p=J'
            'tagOC#mMf}ivo_c1Te_@9gzOOS8OBeT(a6Tn~BPbBUN4&8hq+I&802Zc)gdwZ*4e%23JR(qvivlgx07jADQ8?u7O'
            '2`p;h=hTN={qi7tX2|Jvxxt|l;eiU8+49An+5&Oy1??=I<F~nO|I@1$E6Laf_qQH-7E0q<gz-i-'
            '@#2Rm)5LN@~y8HKp4~>CXeskOZYqO!7q&%&I*5dM(>V-'
            '_ZnVAJ37%>f#JS}8;=~W=gqFhFdYiS82S2oSw_Z|P_PE?niLKA5fd{Z5W^zk8dPU-lq~c)g-'
            'JM|{UX6+GPG~N3X05O_R+6JwxdN^s+b~$3b?Lj6rJbY@RqY*3al+imCJ5A{CB_w({M&qgE=%ZL=|{E*cTi<%_y{m'
            'xd+=>cmZ5D0QRrt#F`HNOZx_^$q4e0&llyqUSP^YW>c^^hA1s(#kd@#|3ie*s0aV&fB!%DD6yseRGM8@<p@1jVNr'
            'us`nK5p>)!4k&h9}E?|Y*$FqqSNhP<O%0~(EiMOtjc5}F+Q<ru%V5{fc>Yor{aS2>5~@0(g`ObCXt4VlO{q%>$o8'
            '>ji1=Kud(mB3Wtw-PavWL;k{kx{X$0{Mi7?H%g%$+3^}O&J_V$<BWV$=d;rIJ736+)MarmdT7h<$_=!Jbi?FlJ@k'
            'uy2Q{dF{;K(A*qSc$;QJ?C<esRLy4yHRzz$9IxC)L%JYUN(G@-'
            '}8<H1{F^vAAgy4aT?$*#D+*fN##TbbHhDS!mzM+<r0=L9Ph(1o95I!3UNa7FJ1#!@9JNGpqf;@v(XWNx!b57XOzQ'
            '))()fvYzaE+EPrEh)506Ou(sIQ}eddjUvbaEDgi<fVV!zkLoJzTPLo=4jBRV-SxEWdTxRU`cWQo|2o8`@Z^?i|WE'
            '^h1y6>JjZUiwgL>s%N-J5<BT~6A$~c9Iw}ig?t|oPcQl_Z(kYMk7^2oE~pP~2{kc1f$gyzV@ts4F~-'
            'ISeBnDG4tknx5vK%Q)zkv~maD;C45mZ`Aoo~GuzPgB0jXPdTj!1VsQuX*tpiJH*&B9vc6OyRke$VO3tw+6#z8#I('
            'B>d9c~QH_9JY{YYzUvV_f=DMoHWtoBVhkCk8o$$zgPX+X^Lp)trH~G0yB8}t90_c?pwL7m2;BqlS~PX@m6b}v`AS'
            '_t<g3+Fum<?Uj?7X!$p)(fLYWO`E2?_#0<JV8hYCDh9UM*Cp?nUsLo=ggRh94HG;92g-'
            '0)B^C`Lzo>oiq5yo3J1ahOXWlg-g3#%bPXiu8>?H&IXHb9Br`;36Ja@or0AfM-'
            '#Sl7n%k6}Tx92xJN5^P|)qH+XRKQQZqKYn*08TM@O$Ah<ryZ?TcF|R+=qJcH1n9SjR2j`mu!Fls4|M}U`FZrwE(`'
            'T<<=7-Op9iC7^{~NwsryydWYM-;+BFC#B<QRmxrR}7c5-|(DL4959O@WE+F^gz$xR&=cX!yN|<Kzb^X-'
            's=9i(7`~5qv{42)-'
            'fZMI1=+*J?=bwY?@<aGxcGAUCJ_C+^d)lQ5jWZrPsbzJy*(K{g9cr^fVmo5)Lemc;iZ_}T^)rV+bXQO+6@U<2cY_'
            ';RMY;KO2d?RF54<=$ZXTkqPT4CD=|b8}ABZ{0vck-y)G8rC;29O$B9>tFQDzBR@;lT{m*Km&5!`-'
            'cA1s)K}e34Al)E0WQ;Is05x7YmH?&zsE@Bx4!`y0Jazy#7GMh<?c*Ad_Ff4UK;?{h>dBc(374eGdVJCc;G5XY6`5'
            'ZV*k@$RryfvT{^YySA!|1?3RD(Y=Pocpfxv?cg0+I8M_A#l9aSqQ-'
            '>#f|I9k<3KPPTubvgtwwiyyPxc$|GDUN=3QRysz|^WBlT<Lt=763RS$BHY}g%gAP|Bi`)~^f)55`}O1l?Q*O8iu8'
            '6`R;Vq0xjEP7>Vn!+ise_N}Y?|KQx3I9#8T*9s_6!xky<7QXmsK$zTMn`QmME_DxccoLkTTFh#>MJ4mBVSS^O})X'
            ')Ez6Zuc^b7VP`x9&2J}$@`!E7js6s5$7Csvg(M+=ri-|dglHm|z)bpSy${{L(jT0-'
            'x6W>Ft=zSSDXLI(3R>;9O3qnc<CP<2XOuk4?(YRje%3qv92bF_TkzMe8KxJ007Rk?i$DkT=F>wYnf{7CmV?zphyj'
            'IX`TrW;n)x`xCCmAIoNEvuOELV~g&R9(~uV%$+cFl4Is&ZZ*vLcPsot<ANSH<idP8AcU%_y!-'
            'X66oP%(O(pIH(qq%B>kD|FXBYV`LXL&XF(B`k5!~yb?cbDxH>VtTS@Sf1L3TRI7e*&R%yDE$w5y{oK8@V&`zo;d6'
            'hYLA`aD-'
            '#YMG_g;@Zj9SmSUgop%eK~8kRpyxqeL!woKF3kS+6=v|sk5bkUHL)sK2cxS^JOf{*VTF^LsxBS?hXo9^_?Llo`>;'
            'Iaro30_k6{xw!7Hx3?4zw)10<p?69&K(j6p10+hdkDpE!%4&9Nv^zlT?^Ja|BYX=T9{tX;BhmGJV1iwU!C0l>+wH'
            '@n<#_+Gd*$aS%GMS7otJwtZ7R0HJ?ZEbrMf22ipViL9=CD}@RE(QJoY6%xu+Q|+ITL=80(*caqH_1X9i#xVCEdse'
            'HjD=5hn$e&)<Yfrys>-'
            '^a}@V^C?BtJdnrRuyhHSpTV9R&;uu7~f!9eS(wS0Q;&DrE%wzYv)omK?Vq%<}Q6vJ>I8dRWNFzs>!BGnFNDO@kzS'
            '5P^K0CMB!DMRo@+p=qqC9kzx>uVAP=?*L6v~yZMM><a?TH1*W~@@G#^N$(i@UmAyu;vn`2+jOjqxSK3c<Om`YLu-'
            '2C6X?2Zf=T)%D+^id)4AF(zsD$0F5=PmPKtE(#4pNeT5s8&wV*Vz(1!1P<(<o@!Of%)}bR<Y=7*m~_kss@L1SGYS'
            'WlgV3dc-'
            '%(vhIqguMn`FP$NSApDUc`P#Md~!YVL)RVW17*ef2;ISo>+R5tY6ahkUP^yOq{ZL&Q@hHxt5+>PV$WCL_RePr37Y'
            '}5Bp8Tw<>?+EM)eVt_et%$U1iSlEK407s(v!lyLRi%lv9i;Vb|HzAW^~*E3JPS4b!cLADc)sW)g-'
            'M<#0xs<*q}?(Ltkdyur%5p7ny2ItN;thYMUJH0Q)6Or9LwSQT*t<~|%#+aE&nQv`-'
            'q@ASRP5V4h`2pG3g{k;esCG6=p6Jq?tjR}%WjqPDv#$t)!MpPMU{=h}C+O4+dkRFJ{|l51eWTx_Qc4u%BT2*E_(>'
            '@we3Xfl%ZdJs$~VbMs<wVIqd>X#`HX?*34BNXLYQpX_4;$N9O80>b4dQyVs@s(w_r=m1cn&Hg&HdWdo|@icUQ~B%'
            'SzUlt9o<6DZ#x%@bSLjE&G%!C7R;vJJ`Z4?{#D2KFeh<id8ff=LWVd`9z*DwM{XjpqtWU1bm+g<)>ix`Q3r~K)v$'
            'Oz|fnJ`YIwbY7LWUXIubdfZMyye$>k7g@BM6v(C<jcFpD|l!R&y=Ui?<c~F+}^SwWY5?<R%gDMeb>xa#W4%)sH@X'
            'Za5k=cp)6huS|4;b{+u{`vOYcS<j8!a`8A;pN}SbP%p)CpHyt`DF6eW&eC!OsPb7lz@-'
            ')QZ#4Ryiz%a*`=%7=vc9{ABHE>-i49F$m}_-iyL@TPzt<`mw4Mt2uP0Bl~!8-'
            'gV|dPd};&f?Sx?$&;IK8XPc%wPWBEWpJt1W_-Rb%G;TcPHl>Rio0WW*bwlf=AEt=aLZye7suhrB#;_-'
            'oCXpmOsVpdW<y>%XeYpOtzxutQjv8-'
            '+7fK%vE)!5yZcPAsZ6nmg{3@>YgsY%3w5O{4pKn%QBtEH=2a!KLFfXq)x=283_u<2!~{y?#xgD^BjiF{b&4S4C=#'
            '<c9X}RK;CJmscN~m2YoK7JpBwtrt;$#VMe>G9wF01uMN=W9U%x09oBI-'
            '?h7UT!$Jil}!c&wq`~pSB3Nv~RxsVoa3_=X(T!~X8k*iu#wDSg&M8IAieIS#>vw3k*GW>GsGi`7>J61f8TAxfwN^'
            '+j8p}tyM(si>X@9O%`Sy8*}M66Kcgne_c8Zp5Fqey_cMAl4cC3U)sf?2jOgKf@lnAoNc;f#@JIe<eX?=qI~Br(Qv'
            '!v*^=sh=y1Q06Ab1rK?ZVvo5Zv%ANkC{K4wJud$V%kv`ntaJk<KO4+@xDv^(q+47~{(g~QPXiglo|R~lEgPxJEH)'
            'piS%nTZN?yj)W4v$049?c7Zd7!1Loy~O_n*xanJPpjgrq@IDjdWxI$k>az~91;he|ck0i)$Lo7H>R%0^gczYxhP_'
            '~_G##?#D!<}w<WljkwvqcC(u|Hx;8N|B6|F4EMuQcY2bZwiS`Z>6E(h}4=x+JJI2En<t{>i%OLkYJ0TWMr|UAt}l'
            'HCs2RQu$EYCLZA{`C?BH3E1PsblAXR4Zav@?hf@?jA$Pn0C^|r3mOKCdWjwVEdwZl*aK=`;0W`qcN!h3+f<~%<B#'
            'Yf13MeIBQuV1m{eo?L$<>{4Y_?YX{h{E|nNvfGB6*T#hB<}=2T=gCvDg6dBrg`?^Ss31AvHOFdz&Otnqd|d2~Flj'
            'O%9ccG74Iz=X1I8l=(8?$&^g%MLM)AC;XlA(n$EiurGre^(cENCt7y6hhD-'
            'X>y}8*Nf>teDFh<Q0An@n1xzvB7hiB9nC~VKVe1B_$PM8H0Zsu?LlIXJR^%08g&6j8`u*L(xGE8ue5Ss)(O3XPM)'
            'y~X_cb|XRYo8?>!?42NmEt5=P$5Noz`X#3_GC}q}v&&J9PY443#wgb54;2s9WDhwnk_wZHi=vf8N#q&yUZI`TdCi'
            'kPu?JN(qX_@c4%g0~dC>b<{9XzhpPy+nYklSf8ruUwS08713b`yzJ>;vJDyUvwRi9>zO+vfa#oB^eXN(vzQLZnXc'
            'AfX-aMAuhiT-Sjp&Oqy<wS2ee;)vuC@5Q<Zq$?nLaXYroWk-'
            '8)Ex{WBKrE3Kc7lQmHo9aqeDFM0NCdnYeinL9tN({La^QqX%ihH{Q~Di-CDDZGrb$2}d8yU1d@hjGwX_Upa9fPMH'
            'M+*{U}yAMe69FyVu;VcNfeN{i!Up1Czpwn-'
            ')kMC+9|J9H8VGYw5+n3dELzB*}JEzO1Rd)+JpyEFd_d;%mh99c;UE2@UeeI1FpjX+B<L@rq;aUCpz62SiTI>oJLO'
            'S2)#cGuNw3t=zO0HT16dC=jt3~Ph;hPStgA7o#SdA}-'
            'oJbGgGpnzdl|!YqNW4L$5c6PHi;>5F<nV3Dyb(uf6(KQO-'
            '7(vQi8wgapNdt#oD=H1tw|@;8YGpK53+7kWQS+`3!d$kR#4eZ5F%335!22=R&R?2GiYKA;BXFCgbnLY<i6|*VYd4'
            '+si)O6TcH~SoANc3mku5j+o@QNo`rj>`N;tUFQ^eR+AX-}Y9OEPbZ=PDbZxCK*QnS!$5ma+>!#^(TB5<>-'
            'gl!ZX<}D~xeQ}gRAIuHWEdFKA|!DbUBiWds(5B7H7FUqn8}Loa@5P4JUuZBtI2ou0dx%5#+uqP;>0gDv2JHlQIGv'
            'zE9}GC#UV0`wzC}316XEmaD0?D4|tQEj1KVoy*-'
            'd6jH`PXfwgn@N$VumxLno6B$?IqyUmhpz{r{x92dN<&Z`+FB%MlII2;3aDB^w3H$bnjawcY|#ame}%gtUZF0Mf~Y'
            'V}lT3lrHcTtib4o3Psa>?e!Y=tyIwqcx<MCWAFv2}ygbhUh9oHN?nS=)+sf`>kK^t4#R_CCH~%gtV?FBx%M^Xp2('
            'gF8Yi1eHMKA!@Ztrg9qR2MFzQdU=obb)Z<Ep@T}Fi5B7G#1h{Ec$;8QV3r*8!`;PQgt2la5`Bq|{?L<hfKm@7U-'
            'NGaM_ohd<mC^7D8b||sy1ktxsFyZfwk;oQ`m*-'
            'Hwgu07avfeeDc<xud1E6L%^l5D$RV3*d^up<mcoS&{A0ySpO<5{xO4LI#Bu_<d*H+!W@5xkY&i{KpKJl-'
            '&KCICX#`4-$o)fi6#PL9>100gdZia=<C%?PI^}4?UMpN%10Y?E%TN*}CkNoTzE}X+WJX7xh-tNI*1I&)F8gkfUq`'
            'jTiU{nJ#UIeNnk{d$H72wbu0;bQ1qh{C8f1~Ydu;V*Jr(xX9_AQVL9>p&#RbM*l5;pew^MWsQUU^ckf_2DX=bJbZ'
            'SO5=a$<i~?-YNapMd=DLJf#}Ii7*Mn7m%2vlo?wc}aji+^p-l;p|Cv>vxO#3h?8?**)Rn7}-'
            'R3;|O_j^f%3O(`#ck4La~U)-c5QRi7XU6-U>%asT*>fB_ASRcdBoiOJE>JSGFWP|uuV-yKIAsD?X`4NMtLEzL|u+'
            'nP;b>jVnJ<n?p>j6E^q%LnEU_`GOtwziWcn7^=nEMWs;!^l7a=xY43n?>ehH;PWfZbm@Ig1QR$hK^RZz%qf)@ZbU'
            'I96bCc*aZJwZ`LEY4;FAd2lOgm*0Y(@9L_1$+$1{2$#z1obp?(TFE!OEwOiNc4a^Ft;G`;M^+gl6L<2{$;#mdI*<'
            '32M%gm1TvR6M!o~*jTgf13!1GJ#gy_NeSsnx~YagC}RX>e7VE2}5PEa9iBf9hVnZY-Sw-'
            'ocH%1GkTa6NLRjz#iVZp>*<-2RHJsTd!am(L2E`$^~c$C}p+5nOa-tE3!qIj_nOM?x_;0xcB7?1S8V|Ph(_-'
            '=!j28^{is*l7ZsppUCVKnEm#)rz>jNW_W^C>PB)a`e`3@=2g0(yX;k=Me?VeEUbo8bJW5hz8x~kTU){($h=|_+{('
            'aMe!^@NUCyFS!1tK5m_?JYD#c7oQd43vOk14eed**prDuved|#dhUNh5LPMmk48tR|gz{rql&xpE}c`=w`PSt3k&'
            '`$cRB}=N_B#8>5)bBR-8o98RTr<5Ch(SFeM<aV`Lg$j-R!^u#bxaCYYG4rv9R^qoJ9-'
            '{z8r!Zy5%#=Z1<@m#U2yyD??eIVo%`!T+`cMnt|AK@6eOragfM7{kFP7*q7H=ORuNR<mzi6S03QzAP_7`$#Ge_-'
            'E@^Ax!%uh^dTZ3JWQ);L!hCDwh?psudb*ngzdBWN1eMX|PljFiB2xEVF1~XiaYT<v=0}i5_C*clhAA6fg&f3Dze}'
            'lE-B2o2d8wytR&EVpjfJtsk#L#{sFKq2cdLLqTL=^FG@R-'
            'jq976D!l$ImA)c6Q8z^|V3~09B*AbC>^tAvPYy&A<@Y^OUAx4XZ!2}&&rs)ldVxq6gbrXQ#G#%XZz&3ewzcg5mF9'
            'GSk{1Tm`v$UPpGUqEuZdmvVV}{#I5@Tc7U=VSO#?63m*5CD%cgLpa(cSiBRSQew0$>=&4aL(*@xFXQUk&J-'
            'PBs+STL8hEmBcoRO2ZBGQi30VFA#P4i8M|i#4k5k$8~+VpB%%#ZDkbJW@<_RG5U>9XLW&i|F5IHxUY4W9%u+a+3B'
            'gUd0fxW>p#^WpwCl)&=Y~zub)?o@@P_lB=P!q(_DUxe#KZnMzHE%qw>QN=;Wrs$cvE(9tr773=j$3it!})v8$poy'
            'F7R}+6(9yBHA&=RKWQhrY7qGi?f#NI)5&udA%MTY8V{KcB8|?{0R*9Q&YaAp`Hj)$tMr=VMJ6#@x=V}*4S;Aur+R'
            '0Qe(SpH5V2L#;|bJQtq+cZj2a_pVuE$JBcG<RTl&A^Q*Z?kA#c@o{v3uKTW7zVU22;q9~{nGg}MtW#(h**P|I<mK'
            'dwnzlW`YQ(sJ@9nH#<@zLP{Kn_5I591=V*Kbm-DBJ0^u0b1YN0%i$Ktn<Q(bcSs?tu@DH$dm-'
            '*49nl7mINWtfIXn=hOq^_k)cQxh6S=>jYnSDm$&#4k17rZZ0ieYW#lcQ7ootQ4&=VGN7Y^wu+c|WhF6KwdX+4G(L'
            '_MA7{<Z;bpB4dKtO9!4%eP*`FNrqrh$ay*16A<GFe=pX?w$jpj9+UaX`Tp?M#t?{;{$PLS@$m;Djw;G#s^uHPNpB'
            'D8S}6~AHRzKez*?bYnX)~)0x22s&yq0n!;I0EW@bqk@Jb1@4HV%}BJ0c@i}^kND0mqeJ@-'
            'zG4CeRqKD;*X)Oi9mPtF4)ujI#B<%&l{ISa42#81coqgr(jpUF(eAe+eM5NzkcE)DNzEj-'
            'X6xil>%eXm4sZd=&7zKXsfM3p*)FqGX{BycJF8pYM~^)4M^6^`v^;rpXu|?#-O&#)iD66iGM;fkdW|0Sw-'
            'WEjhI<<L(|eia{qbRu2i+?Xy26n5_C#cX_;6gu<W|X_EyWxH8B;;;6}RhWu~+}E|$=b4z?y1=))FSop-GoRP7G7L'
            'bYBw5=vlQ_CeN&n5?+Z9mQ!co=N{+1=ypg%(a_Hgl1)t(b4L3W>|qWcYo*Qt3g`Kx?-'
            'y)mOSxEYDK64k;t4k^$fTMRG{Ew^vAlQ>0+2k{Ea*Hjx95n=y%pdDU3VmW5AE&Jmq1!anBOd+Lz(XFN}9=+abhb>'
            'k#^78yzEf7m@ou5kfe}@}&aMoePMVr`DKq-?QtiGVs`-YCh{$PWlqGRvm|>OJx;GoPtUfx@nZ-'
            'j52m(V1Q$Ci(sY>yos4$l_mu3UbdBqpj(S#aP>}N8Po}fjC5PW=u_JBwDoNe4|E&^6?=Wd8U4~QCe1KB%@^+gNu_'
            'Nrny%z5;Dym)+LM#s(!%#K2J%kRUx$Uf%~;dOuk>}w>Fwj8W?eN;_z_Os)>8GEBJL%YJtToO-'
            'A{hMH&n4U`^ne%t9}Q6J>0t;U6cXP8#^{k9#C+KvFu<>w}Xs0g-'
            '}XY6UkJ@3Vb|F<mydy!R?tyP*?=o!B_hpi4S;?%!?0$j)@HuBfOznm-Bu4w@eTpQ!jOEkv;oXCqbLC#Tk0v7|Xy&'
            '7g1QV+Xsdlj)Do2yAycyoasHB>LX!8=QOoCWk(y;{amgbpJzJ+_p2O5R19U>CuT9=T=MC604B862K2E^(B&z~JjF'
            'wb<#VI7rxSs+568Hc{kC}u&4%&-'
            '@VpNqz6wFZd9<LtC*5kNNhRC*u9HGD8+DiryERxY3c{_yk=sMA4SyeR0a)4s_@KqORImx!CbM8@Y^T9&+ZfeY;sx'
            'QAg_>;o!i##+67e2f!ASQMe<Jp85$>+%Aa3y!s_HvPmy3(Evx}4*2aVKEnf7tc@STN6ab!3#s39>9vS_vnQ)qFdy'
            '4EBWv?xMAn6A+)Gg8vDr>jtFM>$DLZ`NR~1DvnQ;@wW?(5SBo0yP57KK%Vo`=VUNe+wj1w)rOLztkcq*jD|lJ;O-'
            '1$j~M}bT5NkV&#O$Emo~7juk={B!&7G0z)t1VOu`E58vLaqqV8Xfzu)p-'
            '_u_GTQW{qKI&<AyR5TCSS;!{Mk~fyTYG@VgUurdl(d~rDBvNPJe4s77Ih?-'
            '_&d@H$%N!=nCr)pdc`@6n+ttcqRC;cZ?T^!woju8RJ7+Px6E2|r;y(a3o!eFwFoMj1b-3!s(U-'
            'CE2UTKkWWm|zwa)(m#}{zU*Eu}T+GUo%ev)Y?hTcvVnof=lg4eqzxQIcTPVHMZ2|UgmhCKl`%#Q?Rnm{rju~aM&?'
            'i^hL>JoEz_i7R@1W(G2DU<ZU&KwszSOsvBm<S`M5fH68Ig8IJ<5VzWfBzG%ARr{XPd*cc)+yyk&utaHZeCEqlANC'
            '83`n?JqY8hf@;U5k=3YiVu!updnNT)6^jd`kfI-acC)}p{Pv5*<zjVz)cVj(Ltn`H^RyOF@V<J?$p)X{IAXNU0pf'
            'R+#T?#|1-'
            'uhyX4ITbrL)c7hYyp8ZLm~!Xj~Vi_}ei=eS;N)?3}?Sb~ASAa#oDXOF+<a6^LI9c3Ic;?6g|;X<ATODO7RvozJ>^'
            '5-'
            'p5mEUT$=c!7h|XwYQHS3V#u)#ADxz?AQTlNK^scW$BTF(A&Bb84(FQ(>4T545<HAEDVDOm2UPwWn8XlnZMoJTY6<'
            'oo!Zk6hvb}XckQG*kPOcNE=meG8a)Z+IA|_duHeE)F|5~HDk9mtM3xD(MqkuDOAy8I#X*WVApOW?=%z)6C1B?5e9'
            'nl`#XKkLfE6c^*FQ$7kfj?v=ZMjm#r3wT}-'
            'dxWY=>o{w^5ovfru7HyzxqrTw?`>HBQrg<J?vpud~iorMEVnw?M}ovLf3vKRWyyW;S5xioZqAZWLA3zhgR|C3b>-'
            'kSMMFE*c>Ms6p5IZ%1Jtl}*?Qz~9fA`NRK!mZHZct#09@-@IlXGT&l@(~oJ;A9<^-'
            'G(&jaBS&QT;Oe9aEUmX`;@1pL-pV{yBzn9G+Px{yq0}qYUuVLhdNU^?UX+=d|ZKFEpo^TuCRAsir!moHGfod5hsV'
            '!kn8}x0D;6@MaU#&jWGg(DV^p9;do5zgL1jT>X6*GTR1)k0%p>fWPe!!*oz|{ygH$Db3-'
            'fn+%WkWk1_r2R{E9di=Ch|v)U{pF%jlaRSg**!{$jZ<#x<P*LTk~l58vNkU(MCR3eq8$S^JW*l}*)ha<*!gAXR9D'
            'Y2MN<^p4=5mnS_gwZK=m_=-<FiCwqxhFZ-w)(~Kueg2tf5}37I#M8DP!*+xi-'
            '4nxS$&SBY1H!u1oYdlQa|!s4ALKfa>BBsgRlZw1+MC@Dl>Y(8=Gk*#ht>sETW0WVsWu$xz(-dD!v!V<`iK)-'
            'prRGeIp*XS%OLgrcb+ym>s|T0k3RK7mYr2vui9;TdpdR;P4|zs~@{-`Qz-'
            '3fUBa2=RuH~24Z=Ej6$!>EQ2^HiwRZE^~19$v9=#9d<7CmN$ir1i&hT*_G?eVVrXnepA<DJrH2>}i8S6115r*;K1'
            'N0O08_W*4d%N1?jYIQ(r9kcx8G^<z8_=7)iI+Qs!f~Hi_?dqiS>xuw$$s^3hg)Lbkk7fW2~M^x(hDXO2;1+pQzs!'
            'lepbh;L)HHW2-HSWe`vc4!P(IaB(l|^;68IEAA*k4*KLr2r>QNA1G7}CQ-'
            '52YEk+!H|Ro61*MxlwrQubu~|kl>Ig45!}y1tb;lbHwy1rsB?Ev~GXrjV0OuP+#YF{cK7Ll^(9cCo^J&2$03zr*o'
            'LS;7MF`Cz%g?ZGVA)z}5Ge5+xnRo61cZ2cO>`URv?j)PN~(Y+S*xXc(8CA2=h-!emN|_-'
            'XNlUsNA=lw4rZe!yVTNm6uorU8B8UjAKDmqVE-'
            'H%_n}5;Ov>S5w_Sb9R5LogRUor>nT3nhn!LW`dKf#qxuOug=vi0USb@{SIkFl;usc|s+hEPjMXM<6FOq*l=^mv_D'
            '&ccq7P2*JNF@aov0~<mYH`f!F_i@s3H{+Hiox&*n@MLb@o$6a;%flzUuvJ@sdf;nKb}@oXA`_!zDB6EsY@`~FQW;'
            'tUDCfGHR|-G*&qu9np)A>JFY&*mVYGgB?YH;w#(dXlk*COIJ76z2f@Nj!cIXXs(2(R`vl_*6JVZgRU#{8k-3o<-'
            'iuepuGnD%fSB@K|GIqy*i(|DH?8a7Mg#9Q^)m5uf=xYHaW{&qUtf+unGtBx2rwuB&958aF!7hpr*7Uxf5M_KNs(Y'
            'j+)+8Gj&Y{^L6k5_$_sK>avRh)5=v*V^DDT=H|K*@`u0B#cmKWE{p;TDA4d7^**!#wJf*M_duEwTQJ6xz)LJx_v&'
            '3NmLB1r!`101^1(XJDw46*+2P%~43YXP<Cb*#RT41(eOniR-'
            '7{7!Cu%S`&w+D)`+Avra<p;Pi<iQo!kqTTKKud!&Qu3sN$K%TyOaByFUMEgPheOJ;$jlvJivkEGnkHqOB)YO_z+f'
            'd+ytKu4S-(KL1ItrSN#f_pHUbD*sNr&~3}zDivABvM;AxS-XLQ_A?C;YP{BfJ#@X%(F2Jta0mJ(D32#BxBdHuf3f'
            'nKk#J$O66_f6?NRP+FcO0fEdt`cKLz+y7}t4lOiuBCRADsz+S(JK1xeAo@nb6%r(3O_6s(M|biu?BAc)ttJwYE`@'
            'u%`ApHJNcWV<5zD^^XEq|e>nXyKR!G?J$mz!4;5aYC_Qtx^gn)Wz8bu}w|n--'
            '!5{a3o!rBJkA9temHqL*@W1ymc<{D7I-@4|`;Q`1-'
            'zue^d^UgG?CqU@1ONW|eEe&A_EiS&{;zZ=b7yk;D*x#PMqY_++D{&g_R4RW+eqim@3DOFd)Yuf_*y*JhzIh0HD1+'
            '=z@x@`wvfZ@%5j$JiJD6_!vL^vM!(k&8v9ALpx?jW+fyS~i}7XfVcEEkzf8Y0p4^HP;9g8*tI25*RF|UR5aa!X%0'
            '~Rm;l_abq!QAkr(S>%v`!F9OYBhKB?MIX0!|DECWBOBjLNoqxUr6(JT-'
            'FoaWxAOiA?=Q;#sD21}X17Qsqr*KL%tFk7+nyJjTS^2C;KA-OOgxWFWsG4<L68n#eYbieuKG#pq&HZ<d3HLAMBI<'
            '^8V{MpBR;4rK}WqD#~?*NhAH+GKs4Ifn;XmV6}!@amGXp<#--'
            '5z7G&5;R)TiRSk{)le*MF7qYxEO?iU9K%vOa|$w#Z#f9KV=@=0+qgWSlq(ZeEG4<&uc`-'
            'hD_{&B&&_4{ZY)&7cH??8W0vt88GOQC04*TtW<D~wJ7%qD!aLR$xZwDT35i*assrwya@hi9_*0_@cPe(4&pl^V&x'
            '6OGXX2gvp-|<H;R2cEbn1X-'
            '#u6|G$&;g}hd(_(mAHO<_~!7%5uCF8$<gCyFAksQ$IlNRADskrEl+78L^+h*RS*uUkhnta9&-'
            'CsDsj9{4o@CGdj{LY6SOW)4MH<G%9`+yZf$++<eeIC4-'
            '52~@1eHWZir7FFl*C$lT)C6devgQM2t7zG=!Z6`pT?Jka-vx_keB!P%bVpW2U>+3O{?&b%7uZV?=BGOW^9zS)n42'
            's=1}{)`Q5zkHU8c&YyU<Kf1ApyqyYB3OznY>{N?&rHmweGz9)<v=Yqr9#VbDczbL&6`KR}kW4ikmZr>^>Cg4a!Ty'
            'U2r;6328dGLLj;q%e8XQ7Mn#$j@*^CK8|MHh#_8%nk`7n9D{}BHBm%nI~q;F65opF&Jx!uu1^=i#U)<l^q;&a{(A'
            'DzK}gw#PPe`SvN%&WtOL+rQLCu>SvI$ucXK}zsGAb8XF$%8B1=jZ$G^VCmxCr0b|Dtmp(`vON4Yg7XalLwjA9NLk'
            '{>L$dOgYcnu--^sCI!nHz2d8~_i%rht7$(~AdubmW*X3#)K$&^5Tq4e_iYuK0B!n_-FZT60;%j2_?GR4rKtuRkd^'
            '-X|zbrP~3!X5UtuBj(v`6$JMK|guZF6;ya}B!tknp>2B%s-'
            'e1uzbES{nE=xo<b&G6!m0qtt=H30Ylkw@ZC50B)^uSyU8~i5?0Xi0!;fY$thd+K)M|oR3wtvMVVXyM~R1$$*l43~'
            '6c^g99CE@g*6{AG(Xguj6+IA}2z2COByN{opL?KBb0!ktZR&XKg<vc?zAj^f;8Rl-'
            ';WJE{69ux*o!ZGgBO}s6Dq7$F`~Fn;C1--LujRB-'
            'L&|w<N_ElVrI$pH<`JM2+|Yx<5gpuURqnysiO<a7j{dp?gY^e?c(X5rYGbv;%qyusxQaA>?bULV@Cufs86tN$!eV'
            '?a&-'
            'Nv^!?u3T~QpP;~N|UtMhGWah;A4l=;llxB6fm^=m9cU>+fKLI0}4zoVyc2mvMNqc#ggRj&avQJV{+BC%bUBt(QJ<'
            '9Yeiu-BXqO89&dP7f$kf(<0qb|_ukkIz4KuOAi${H9V7SNPyX^S>Sw$7AjD(^zW2~>ZN{6K|x;AJjUXH#fXe{D#C'
            'DmWSbpd~PiFWJNAj(p{Qj&txko-|Smff`UW*$6q}J_AhaA()d>Ur3lpw5lQgKI(@c`=D;aUaE*~)DV^mqW#-'
            '3Z9q&Xk=!@rV}&C27@n%aX^=5HN^=lM!$mTLY=fUJ8*w~*wbfAE7kR95ZPktMN*jgua7*JI`!b`4o@i)lP>r@4FA'
            'q9Tg)zLA&fH;Qo2iw#RLFI!58Kd?pLWObzU*B9{+A<KrER#g@W2Xp;}ezQy^V%W<E&dNF8Wi=A;Xct9%twxN$|}q'
            'U)Qq((iA_~Gu#i(8{@?{L%V7-'
            '9R;A`Ie)T(`wF;~fs{!FSF|q$1kIWZd6Mwz1hX>1T;9?FI>x7GhHp6jbX~)_YjSmoRw!vSmsA&7+C&^tv0x=jTRI'
            '#e(8@WwuohuPT(c}czm_>Ew4kCGM>96mO_u3jtm1=~h;pmxxbkMkmFt9iB*9Y|<Vpg-'
            '7titWC{(X4<dX*c*uXDd=;-'
            '`R_gPg7PC{eH4QOa1li_N3!$?&@`H8n3lR6u=1Z!ByN=@Lz$~THBOTTXJqEK4~?&`CLjis6soqP<#E20~(*^n35T'
            'fp?w<ur?cGlIn!nzlbjWOxdnP}Pbi$*Z4V;J!ASIae!^PGmx;FbvV?P*koo@+;qTn`iVUig8!!*|7+ARJ^058xa^'
            'NM-JZSL-FtQRINb|k9q?%QraIBYDZ&cW<Z2;Ecas}EdLXYdxP}p(F^1dodNGBX*r+3t~HAke@seD&p`oa#N9We5A'
            '#`S<Y5`4FKQGEHuLakSM`dj!J$vrsK)$trdO8m_Xt)PVNnh6=pAggVkL~^$Ma(KP8@_-'
            'm;yH;<AL29re<{425_E_ir+x>jngyp1Ueo_`z&`*9PdV^MapE?4Y?=zM1tUHx&*oN8m%ZYApL4ozn=qc;+-'
            'qvU3gj%`e56iBe^?*#USt>yViUA(<z7x(gsv58gw&GZqyFnng^9N2QsfmjI<&9s$dtKuz^3i<=ee86%p?(%$~aaD'
            '}7n}&MgFQ@{^jP$~{4~JCFqo@gVxZ{$2vHIPxR4nFrwM#`Sv?xlQLBa+zs&=oOwZ#-'
            'lb~LJ(S<I?epq0)69Da&I7tz?^vGs6p`!aCll>U{-I%atOy3@`hx;mh0p{>vKz{GyJ>)=i535%FBlduIm-cPe+HM'
            ')hqg`T!RcJ6itAtiJ!xp`4LMlj^C5clu&Xzl%7IbQT1$MYFE#8dM3mXc;|11<Fang;lMvw0#T4npshI=I7zawu%O'
            '479?*5`-'
            '|HdnDl(oxR&!AI)0+je1{0}3fj#jW8EA4aFiAwYfD3(vS}Mj#<zOe4Y|w{n=oSP~Z3yucnBUN2=aRwO(?Xn~jYpI'
            'd#X_vMfJK*gKzCywlQaSiywAtW%tolQ0YZ6m1&FWyWO8GD&#}#eG&qT7Rm!%!+ccYxcUzmn*aO^13M+wt$u5XkpS'
            '`*Lw9rxpNegVNvgig{=sp@IhVL){rfA4VJ<dl*Q7u?!gk3K~3w2IKAkN%e_kn#x+8PUD<+ITNu14;Yq)47v7|8jj'
            'pm?C+8E%B|J<yQ$8u^ev@E^t44?${*23cfMjSIU2C5sQx9D#_6EcT;LEV(O=uQ4rZ2A1QO1+%K9#3tZ~F3GibJJJ'
            'oX6HP1?({bpJNnM7YIG4r{;lu{KoO{!?3&>AILc)2}1HZkSq}=%8Tf6s}5)F0&33a@Iv*i2afp4woLs5LHBKFE9E'
            '{qz<WW$jirC|X}Bcn3ZABlBhApRP;HonJi9C+PJ9^8)Fay|GV&kAAX>Uin`|GyC0{Utobl**0CF4imLhNTlOb3N!'
            '|q?A<xz0nI=jP_Gga#91?W*1Khkl4%OeFX?fZoT?sNcERbmBn~vgTCrja|xf_EGl4(m31b0SpwgkTx`mw0dO@HbG'
            '(S8<U3InGjD<dH^j$DEsehg<{Pz1*41p5_dn}~T2jvhXhx;Ly`N|vjs6-'
            'M#6fXOYG${V2~oGyQwpeW<(cB;ymcq^R?p__%w!zh<71BIpZh@Axp72|zLE3!sSh1WZ-'
            '^7@kI3gHcGzyrrQu;hm6MCkjP~c{xYz({VvJLGIBk>E_=}SP@fh9d#}!8WcO_==4{QMc+@tHAZPI~RUCir^$%nW$'
            ';4BP`4HLGvkeq>zWOT3FD)}Jh1VoP=7o$c|ywVdi)Jt($B{H$tlydL98SD3aY?Mi8q*xEr-eJB&-'
            'bKFK@%%^I#6wp!bbh<G4nsoZg$qSfU>zpQ6_y@@PyJ2-'
            '5z+c~yq!6PpcKjDgidpe+8HC7A}0@IJjoo(&Ugk}lPl<Aye7?8X!C6)OtLOkAl-?eA!+c0H`-'
            '#(@p2fng7GNm^SP)OyUi7fHB!GpYd~ya$rryTu|}y^XkM}0%3>T$s*KH2OE<04DC0ZNbv7Oxn4Vt3-'
            '1xRvQ=QZ$`xS8oS<=f->M{9>z})E@gDg2be&$yFOs)7iTI5y1W3ddX2<Z5-'
            'SX@w`HT0m+Qihi^p3)G&|2K=KnEH;{6e+LT9mwfP@Yt`7GwZ!j``#aVcHpEq;^b>QDUmi~dLac?-d-'
            '8ALBOF1ZLjocy{axSau*XDq9(5C#tD61PDG#7fKJCa79`pRli*b2`Bw36d@C6c6Bp||BZ>UD$gb{fyap3l=E{Yvy'
            'xp2M!UL}5Mua0B@j$6Tye%b&1%gqquT_P;kM6JwY+8pV%3*66VwZEXp?mvki6n?aw>fJVkpE@9DpuF-'
            '!9w)grGx@De#YW91m}H1XB#Ill4O7gh9V9WZZN?KjqBz0D4~Q3rO-H&W{K>xVz}k1o@~Y-'
            '2~ZU3W+5|`fH=@x7C;|i5iq_0HmRsJ!H^iMn0Wu(xL%VHlnJ^~jybn+uKGwPozAQzTcVhsqa^(0-yKBe-'
            '@`x9n^F{S!=KpFKTze5>Wko-nts{16w^nGiO5H&_L&gFXR1>VR~~8FYhO$wSHBlI_X_E3V=gkEnosyt$KKSPGgs#'
            'sbLitY#<ww&2~Ha>)4iJ&E$|P2Tez0E)~w}gI~V#c`DU(dtz6Rk+YzSu<zMT1p06=i!kSfb=x!$RfQA#{xXEeAL%'
            'RlE5ZJzG8XO~!jhe<2Uf_>FJZ9QQ@;RW4!ORKPloQ9eNW6<N))NEd=g1H*E-'
            'ZhYnEc?%7N*?MAC1Haz8cgm8{0>)me;gvG-V$ohoF7Vv^c%;gKV2S$8;n&ohwp-'
            '=}*f!t~m{E8s^|b9}E%kBf7k(xr>>}O&uG@>D-!b)breB`t9MeZRm@{R-'
            'LUC;p7ScH^xM6*;|V4<rQ!Pm_fkfU=4cYRz#Ld^|7mmV-CYG<eg(mX<Mv+OMDM{@We%tzLKUTWM*M%<v3p&6fexa'
            '_;k)oaUP|J2<+Eu#9CqwUQ#=q87#oHgr?h`lBuO{JR#E;$>Ece`$sQOaCo@)@Z01kiY7=NjvfFKH<uMD{BRp^@_?'
            'zxhyX65x=s>gV=x&2Aude76+xVv5$UX%lidYQwt`_5TSD9haUjN64*xCKbU+!tix&lDj9#HoxGGmk4dP+LiGYEtf'
            'fmM4N`Mv@i|`L>))-'
            'e)Q`j*j9>G;jt5vgR5nz{9ZR8?kC`L@$V2gU0@lBNhN`0KZS_rp1%{wS4a6%}~Ktg217)>fqv0U{OI0+a|0D$NVd'
            'XSB_%bn+?vf^{^AYC*bDuiRTK|)*>!ys2?GBs>wUPY(%5qH=&6`+_8><((oi1D`5)VHo}$8t;!h$CKa%5o*Xm0B6'
            '>!`exU?{O6b?&PIn&ENtnsol(*&3s-'
            '+EvI_CA5eq>6|C17)l6zbDsn@S@lLqAVqy|D)2J~=CVRuaR+)shc;a;lsy$UFk`rQG0xHfOSN(4H45>Y{u+Q2wHC'
            'QXPuKnaj{e64?#sk-'
            '_sgIjtg<ClllTn3H6hNFF7C$Q;!f>J72mf+<=+&Bi(UV8LxlJwgYY<B&s5+fBpAJh@YAbY{-JNo#Ch--uGIY_qx-'
            '4gN#kk|_8q7IF^_et}j>$~PyxxlARm&tZBXKuBrl?tI57+*E=-6kkg={~-1mmU3A*#|+mD%=uX)ND=xOZmR-'
            'x&{;!TX_;W0wY(=A>yl8jX^{jn!uttEwmSdR1m==DNJ;9C$QPrgJd0pEErP0&mdfmmb^RiA4mZZCUr84dNcBU6aD'
            '#y#2$z?c_0_&OBY1cMlGz=OMe*LSi&1vYHS9>a~s&bLP*UG}4-HI7=y`xVr$29qkh#tZkjX>3$lXb^65gP-TzZ|M'
            'EX?4D@#Yo3qR!!s)LI(Se3mRwFkV$PyEPU9RWi()M%h3IAQn87rBFH`MnSp6R#wVlzK4S4736Hbj3xQ#gJXrhY>^'
            'EGhrU1T)4Ys8$E92eV!<kyKfAe%7@;0$FL^5VK4C<JF37@yaBA3A`-'
            '4+aT{l>T1ejMes0Ef7Cp0dP+ZbJSV9%`5%k(X88#AS^VMV<D917oqvCWJ2fhsaj}$vcXr@ScKhA^^Y0JLyUps;n('
            'Ie6A;;jKWrq7;d*luax&u@iQLcBx?@J|lA#hOkLu3l=^zN8XebWGD%s5TS7Z1+ADIe~oP6G*4(HuC6az<aK9p%<A'
            '0ry+PH@1B2{9hi7AB=l{?Agno51&7KB0twU^uPS!n{W2|uR}_!W3E3_t*=ebz*Jnt%npb##MN&>S=MfK6t}YHJxt'
            '7#JmyBg^Z0#kWn7ZXtpm9IU9-'
            'NPmEXhj^Llcf+}r?8EY`rJ%qx&^;F?%8yA7tpe#9>@GyZ<^ucL34>qiMeWIy==#NP)GfBz`CMW>+42Wk{<{D9g5Q'
            '*u!)_LDvM-`C3z$)0Gw#MbiV1NGv&`(k3>T|Tf6j7badpuqc`@0Q=gxsu}GKAxV$>J&)zNe)bWOvPb^AxOu-Cqaz'
            'jJBE-~4v4-'
            '1o;Nt8V5Y3`8u8E=GSv5RJwLA&tV=e#kM(n7gzxSz5flkQ?jU8L?t*N&j}U*9B8>bbWKA;I%riN>dg_iQ_WH&=47'
            'YMy&5yu3TpGuHvfIGM2<**p$KiW`l1ih-ciq*hT9=yCVU|+Hfc7d#EjOUa;QDvr*+0b9W~WJzP9M{1O}-'
            'Am#Z<evRJzA(TY$<Se|&vXP0DYR6{{ozF}oLK(~|fsJzOWKa^+NSGPSZ&-'
            'U?qURLuUisZi@esYW<Iq%7cr#vL(_(d+eNVCj=;PT5vpzbVJ-'
            'r^Dp+3D6My?>f}uhfO6r=sWiHW5iAEkMo)m{2RY<o1Yigwdux05Aj>pBT}T9PbSk}5FgEFSVHoNFgh#e9!iKyEwQ'
            'G7>PB?PuQJIksfaCZB?7mYG`o~%cz4{qXPuh#e9*0_)Eef_HIe8R1f&}a|8KpHZ%Qgrh4CQ|zS(o%N>B`5`+tq(A'
            'I~PE=Ov)qDzkLo_9(Ab=wir$C<fR^#`DqhVlg3F&~7Y9Uz<!mme~~9MrD59b)C%QP#_&nN`+=i-'
            'bdOA{?pdii}$1R5=hyASI|D0sXZH!rQDeiNF{dO@-z#kty-u}K^FB#_&t#G9O-'
            'AHlX+dQFORDa^J00rf_oXcz#*|*ne9@Dth(|jRNTAm#!IK$FY2WGl0MJa(M5TM8yKok)5oCBT&%r^s99H>HZv?;U'
            'gS;~4s^JxCS=&*G!tU7^l;#W-?5NXRu`9Rw>>{~JMi7+wq5D7L-|nlMh_p_8jK}tcsl#-'
            'edB~f)Oe?aXXy8S@U0gtg^n5$9tLoBlZT@{=)>!=VJKvu1DlRH;k?`kar8$eV_JnFJLFNnD5F80hLL)RYM^if8(Y'
            'F{$a9_$J^bFg<YS)--'
            '}kLECt5t*s_3N#Gw#JNgu~Xh+RcIg+pJ(R+|9)sIT%v!EQ;VCs`+N_jbNS>Lhx?_^UNu!DCR2)RVc??*^%+@Q$aF'
            'n5L`kxi1bXuF!;)vqC*4(y)E9mLF@9>8j0%+i6kGGp*T3<*7S*i`Msg__23pyR>jq0-'
            'q|J;jPLLriq{~fD14?=TJYX4EYu1&34%9()NR>8B%pwT0cV3iw=W$^UJvpEWxgVUd(YYCdy=FEIx0-'
            'CirguZ8YQ8jU_m|Ht}(4$IjvorLbt7%d!J*(K8o~W-'
            'y}Mzv4_qcSZfNwDOeet`CE}qLQ%~Tj}@t9PA(&%w$T)wQY|7s*HOJ!)ioGZ&CAVf7A%HJS&6yW-htrsxk!T`TUlE'
            'daq_~I^$hrnu~38<9a36|H^_LtKn@Wt&Bn7H1<%<zLhot!=RXX>#q;hZ1FN0jS+GvEu}I0u0M&dLJIK~B*F8TcZv'
            '^Li>Y`}-U|@pX4duwg9#EDv1L-8A8^c|kkUjxQ24j5;Yyb;|1Em(s+CPe$Yr(6%`DwIty*Wl?_ZBTx?-'
            '6HbB7)}WthnG`kI}z*747t2*bS#dJ&2d6SCd~>#WGwczLNv9)ri5?sONlHYw@4S75cS`z7r8`P&Go)oDRGB`|uWi'
            'GyV4KZ~ryT!uL#kKiZD0pv`esQ{4=GZi6kZ*p5*Gn?nL(3tnWQ+&IS^t!r*-'
            'M6<aYa9*CKK@p9#pqj}Jr_%AfW#mSoku0-'
            'RPG+4%t46E&qP0qEP*y*+<#Oq4jcftz4k`{jIbEisWM!w!7g<e&zpu<2Ce-wSa#k3g61Iv+)1G17FdI8&4cS_lC)'
            'ki^S_jl{n0##VNO`)&j14+FYg6Vb>+S&ldT;1ODVL7rxJ=7~R@8Cy5(FY-'
            '%EV0RAxe>|!J!zLQtcc10HdPXLHZ2wfc<V~*BIeV9$6SPeeEd{DVB-#qROk0)M6vko0TUrDkc-Pwn4hPD|@6vSyS'
            'vlDrpa29zOr`$+MIE<>8B?_#oQ*c6S#&uXfk<u5i#Yu%3%D9;C$S=Ia$E(KeQDfBD~Ey?TLZTaW(N>Cwy66W#E#o'
            'GlO1X~ilo+Z`5T-'
            '6^WP&>B|hCYM?jDdpB;0+4qL_Sg_B<ISgsxI*52r4kd(jRU(vl9N8WSkx<}O1?iUHdvO(NFOb&+`{N7#<4Bhs<A>'
            'u96bLGQ;jJ@_(15S_u(QFXW7wuQ<X;au|#b-'
            'tKTR&A0rpLL<_yPSt}QgelA<HWAv&dvoGnDX<dv>%h`riKLaZbr5uxA6M?eha{c!~hMK=!%rL9VwF*ZRxdk7=h8C'
            ';wC3`(0kc-8I9RtQY0#yBaeOY5s<#N1P3$Lu^x*6#Qx+tvd!CHSfyYIMyteP_%kV#2%c00XZV-'
            '1rvDjWr5(7s52v@|uwHuhj7Un2<_WM2P6GkoGk?Q`He<>Gy{s_6<$gm5`AzG=LseV0vc6?tb&$VIX^bXlYllCAL~'
            '!fF3w@}yB-abZ(OH*9p{Zp@tWSkky9+C-'
            'Ruf?>a?_nu+82~iERsg>d9>)j_zLRRIRO4U`G`fB4(n@Oh21j7tksL?Og1i1GmV5>Pihb6-'
            '#o~_II&sITR6BCT5TpHSVfQ6I2hd=(Q{@|H-'
            'o})$H`2B*fQD|zKcvkfVpi1KndAw;Z|Fl`Jt=XL78RON3pW?cVH$OY`QWgr+{ezMqU<7jRJeO%eWQcYF8%?MsErr'
            'h{Dh~vlGSg20sBMlJkn?;1*f(`Zs-kn7B~`IjZS67xB1g`2qz;r7U}`tPbAQdc@Msf4K&~+^iUX-'
            'iS!tj>xtXyOF!gL1nwm<d^Ggn!intZqyiRPaR%g)8A()v|d51YAt;J3nT-TYGKS?HxBsnS%WU;U_9jWhv^z;j`?D'
            'dtj7BUmXo({^ytS~3}KmYsx*7n1ZX+N}vh22NJ%7X`cd&A^gX+#Wv`9(beUUYqpVvGG`1S_Jy!`%<p>s58WS(n@s'
            '50rW|`sFZxQle-7tHonX%q?wU)<`otY^bl%M~|`JNlpc@-'
            ';8Bi93~ZkuuzUUrYdGvC^!&;vj?KiwPJW@sOkhjfCat=LPISUkHbAEtnWm|KfoyE2c(A8nu=Cm028>9Cda^lmmo~'
            'eP@qIl$@=P1@)Vd!s(R1qjWAln;w>dBB2G&=8HI+WNts@v+`92RVU2vlB9bXI+)FdU9{D86ngJHV#ks**yb>Y626'
            '*L_3A|)*@ro`{UMSKyToKYGl)t?hwdEW%5rGg`Xif&UomHb2iV2LF1GBG#hRQ%Tu4kJ$GL{d4Rc6uIBJr7@yO%w@'
            'RY!NId!iz)O>F!RI!|IW&iR`6%<s1r0TAZ3H!zY`4U^wT)|y2IBTFO58h^#Ay0ah27(gd7U@Updstxq)mFyP${gv'
            '~np>e6e-'
            'x`P0vle8qXT+xwHup~=S6D#9<gzm(uakK4roL*n|1v7AxB4n+xliB*o|WoZ@6R4hs`V*XXKx1nM~v4%#?8j9YpE%'
            'tuL$xVi0B_LFCb8@p%(oOzXdlDS~#D*RY0IC`Tl-lRln$w&tCp>>sKQxXR{`FcS{*EsCJ9#&sBThVKCC=tAPy(Dh'
            'b0;yV{jEOLf%*t6YLOnBk#;V6Ua4R~l(@GA<Si<oK)*oY5$x?mY`unPW0D<Vum&-'
            'V<yCTTgVGYreaz_dr)t3H2abJ8)p9)v~3fjleW4p{JZF6>{5&;XE@+kEv~QS}U_}^pJ>@8;@bNk6H8|jqAk%EfRu'
            '}lqWeCs)3GsNssN!64leIn()<-m_jon-CVr^tRe}BT&a{iG)Rxd>ky;3z;ZL;ZZF|gs0%7Ya+O#z+}C1|LW2O46X'
            '`0Mp-?YE@4T4JB7Gm@`{Zyo3-'
            'iRJUGL}#hxho&)9AX58@FZU#tjx2$jX7yGADzV^QT1IQfx8!j$FjvFt?R<Bh6?G4D34(n`NtZ)QNOnc!xHMK#>uw'
            'rmbic82}p~-`)e6A|t3~T`1MnKgZxMbdm0jTi%E}LE>ja$rz@Kmxv)^-'
            '|u452k2xBBbV5gH{3wnFvzGyU%WBy2w&LvX@PyHK7o>*h-n_8fVD7XHLI><SZ)i;kQL|8a)i28F~&vR)-'
            '^nJEe+xZni*?)#DbK{#=)yjnD_5B8+-p-C&Z+Z?Lfr-42hlK$gGz?BumVyD<(T6xQ?X)l-'
            '$d^rV=>|t#f)}?3~I=07x~V)U}xLffycEt{8NcIiN@3j8JGBAZrf!!Zuv!Pzc1`%ZMJX)`c9=krL3=0qkB99T8!<'
            't_kD_WPojO9h*f{&)&1#E}}tqDO_EFhh_EV9p%JmT^MqJ;>xK)6=6ab%P`!^xIH2*LdQMQRG+0t1DDoEnpqpwHZ2'
            'c5BaLH7;5RqPqGPBJS5-yU&|o9EXSNe-cCucTSpD)rj2#v1rR)=8nML%vR>5V_Hrr}v%)X&dW4XQ+0y7j=KZx`9='
            'd*hJ?xea{fFv83hb24+$$zky^%~7cjS<kR=PMq`*6;&Vgr<4mbsQq4=0K*T%bmf<!4@_XSUT;uFfgjD*-'
            'Ju=<mlE|Ml)7hDOoD0weq`5=jeg&nxQ`$=_V**cxq914R@G772|hU4s|in4oTyGEx#TA!F5QYnAMnHN1tJ*)A3~T'
            '&>wdDai)J5|2~bY+e{JFkWhQ<2{++7$}05)Y^aNst!GOaqhiIQv~pJ3S`NC)T3IkNjJZBxRM}*FA3xGI4ZAL4$2t'
            'VFQ-4Q`8;L~c+vQQXvvy3SoYCJC*$yxd7<G%4VchNnd-~#t?=dIPZUTfQc-'
            '+xe5K6X@_S5Y|T_ttRHNz6YAxh`S6HU=ENq(3zb5*fq`yK-'
            '?c%M<YdHcje$GD__LY}J}9q;KC0X0md>H+2+N$B=5QwR>%6ZFx9kJ|$vOvmCh(OX`0-'
            'zbFA&Y*Z}Vni4eciGrZjGT%DCw{p?H~Hr6r$Vgo_0{)&=s596uC!|xX9j9bqGEfUS;?mi`}>XV>zb!!%3?Ip9t0G'
            't$bfmbzuD<~%cZpSsx!J}p$d`u9<c92XBcMAjKPRWi*Q~t)Ed^dnTyzZE4ws;Ts~enjGAlhWd4MQ3KaS9#zr}iAH'
            'Ur@Q+!QOksq5vTda^wvcmOY41k>ZC6p=S%Fs)(Vw~xavFG;S#<KR@rakRF?UG2CzQAF=tgp}<BB~{sXl8p*^UV$9'
            'm8aL-'
            '{<;YHVL#>p$WvgSsxJk6XkvY3Ioun8Lbvy=Z$FawaG(7AF>#uB5FGGc5^<&POuZL1vN(*?FxuKQFK<Hyr(uSzE$B'
            ')6YkJBNEEMp*6j`Ur1%|sU7M_BmE9^6<D@XIIFp*lMDcS4LlSeuNvL)Y{U~@TiEmHboqfObQ2<ejfF*=W~Es@end'
            'ad@ZzQ{QPryvP|B-%>w#5Z1)y5n5N3^6QkPyYFRq-vH!oqM>g;gq^l+S_<#c&CM#lHeHfpUr~(f%9_|B>0zk$>Qk'
            'oW7I9}*q#H1V=lU{6pL{g3+9R+tDa>utuJfm%h6S_LX&a(qI^X3)y68d07EU2hsrI|o^}j$YU+5ER$Ru72&1biA0'
            'z#{($+zzshW+@jT#B-<eu;Ux(HXL?%o5<GW7*gb5(&{;{;kXYFVi0R#Wa;n*-'
            'p;>caI)`>ic{WaU4($N(O4`)moYi=2SC3+Wcu%@!W3ot~>9zfzY~{z(8jiumxa0<)ni3Zs&eSQLnvQxPt8z)p^$1'
            '_#TR>sqOW29X(&oBYssbRVkXe=buOhGVZ3#uhSGD#yR$K96Kt-BYTp0p0EDap0<8&6SmWd0>&)By0k{i;uHlZVhd'
            'w>A5E(x&{KgvF{l=U{cMrDP_g=<zLD>cc3s+a!&BmK;1}wcV8IDL<Vlgv=-_zO?fs4Hx^R9{nDE2muJ6Q-'
            'S*bA2ukAJ>|5ModT-3KD9X|+SKmVL!W%_&p=F~~6pstl8`0%9&H6JtUSwv6^S*0naJ-'
            'O0_6Ap^9VWSa#L5Esw4P1OM)=cc(9am5Sy)Rfx2G*hV_OKsR+<CBmPerIT7IzgZt}pL6>{*ObVeS(zs3CS`SY_Zr'
            'LEB;&Q4%jj=f=Q=2`1^46e5uHXR>|+7Wu${_dno=PNF*Q177!H@W0$!D(MHf62~v9J1DOdm?Pw)uXRo+~Ala#b~u'
            'gJRt^~LN!&vLe2(eJ3#bF6~WXk4A|`oq<%i|JGxveAUl?Pp--74`41*vuw)i1yEod~Dd5jf@qK3ye+nu1;{@G)Lh'
            'e=qZuU>P;<L&X-iJF%wr#)VaZ9c~RN;5F>d6{YZ{$I5bc%82;SK0Ogq(}{_D8@d@^yTub=EefeGK>9TldpKQZ?5-'
            'bAr-Z@3meA&bSIDN*ntHwg!z9zTweW%<i^U$iD6woy2^K84h#dtA#>48~Eramd_&{vrDe?n)bfA>-'
            'oLo`T85<9`27w+VF_UpICNsRj$|^Fx`M)#iSz|E7Paq8?YvV^rGQSM(#%#toKz@oufVi>v>46<jEy<r#X`oC+c*b'
            ';^yk`k2EqrLyK3hFOl<;RbJcllrgb&r&VL%C<+7%(|$T)^A?N`B_ZfMKMXF~#@Kl6+uI`L_u{1@(D}rW*%B&`<W>'
            'iVGLed|ev4WdoegZmcA>FuEYfoODA-8oi@4M-'
            '*ZfLU&98$S`(7Kds?seDb{np%t7K29#cPu_gQT*LiqLlq{Yaw4`W53IM4hG;NS;zcfdP%_3EIkCxm%cDZ5Bpz&IS'
            '<~OhspOjLPCY=C>IpTHFUgO{D48IXy6Z5glUi31y7g=|`x^izbQY(N8$xe}H<4EKOcYW0WG%f50jwG2&7ZfzM;UG'
            '3?SLgRe#yk&_O)6J}bF+3!U=CR1726pJ4WtP!$N`C$ns0?UpKGR}YMWxYkuF)_%f*-'
            'WR^htU|MooPLr3^J_qo#OP<fPaquv>Jf6pGO&RzpN9XWM>zt;-NqPt&qzgy4#?a@3#L>1pA~2W&oHmDT-'
            '*})=XbzAFeIZg>!#nO{7<2(o#wWDo}<{!fW<fwUDkRtV<8pTA<M=acDWVga*2YwbXuH*eOTQqEC89^x3(qw8t4<C'
            ')KKym5s?AN5j==VBlf5M$PUzn!kg;F^vYAGY?2-!3ACN`rSbwTIBC0l#6&g(|3~+!m6dD@q`D=u-'
            'tV!C>1FtKVTo|gFpqReZf*wu?*=%&)9S8sQOj5RGGCYP%sFyJ)AjU$Cp45c>k!h0JPc*G|H!dCYu$iRMOND3pf!O'
            'g<e}p$p+!fJZP#z36BS+UtQ6Ck;Dw?W0bpRfj5DK(0KGbB9aYzT%}oXy>7y))VpUnf-&vt-ja37_!%GNMYX`{1y4'
            '3BCU<+jW3$*pQEX*k;Mh<=II{yZd_V=&=xQ23p?ELK$sm&X;vA0JyKv-'
            '+DCMA!!&_s9X8|!?FP@_B;!g8Zg>gbU_0kCYk)$!{dT?Wc(RPdV;dPrK&h}C|=+#i!s)6~LPvB^RR<PWXngQM`kU'
            'lr(VW6$jxBqdt`|ri>U-x$ZFv@q&?xFi~o=RM?MR0$KqB2?vT~n^jD0H2XdqXf!?ge!}iR~$GqPv&-'
            'd%vIDnhT9><c$xJTZ4}oEf*JkHZJNNxut#SAJm!h?lz}SXm@I#-'
            'W}{uceX+G^=s_5QJsU#v0}eQ<j^{O8ioHG6S#nZYfHd=to5ruGPYa6x-'
            '4Ps*04KU#ClmXx3!Gj$vXBi7P33oWIaon+RQtcQ2wTt?=9?Dcd}=tJ%+h^#GTR~tuJf5nZ<8QNt-'
            'X*+|EA(pzX`K?`CZ2U++m4ZToc`=HG@Nw^2je16&G3Y<y@NPMWP8;%yk5wm<>CH*9cZTQJc<Iqu$plW?=s!gVB9A'
            'LEq+XC}sDS#W_X$-'
            ';89U2E*>X^+w(uB==i{IoCl#<7YPc)*!^qK(KY`Jnx#5ninagO02E#C27R8MV6Z{C4UkUbfu)eNO#B7Xe^Jh%O?2'
            'VD36|AZcIH;Z_k76;FH0m%a=Y7Rq`RWRhc19-'
            '2>_P{mZiezM#u_Mk2tZL$(lrq64@${cQy^|hrR9JEkvS83#GjWmxp5nm7=aJ7ui@2m$c;4Xk4@jC-'
            '`xR?%#nhJxsocJSRt!Xx{wlC(ffC^Xvr^u-yU(O&P<AIt$4>n^I-Pug9E+3pYn@re|BB>U5uQ-tEMK(W$w$#&W@k'
            'A5EsOSl|v93eajW!}G!6gf%h|n(1{iQ1J&Nod=8cHd^71M=7mugzc3}?G0P)GQ=G%^>BRCo90MUrLdVk3v`u1BG-'
            'gKI}E`j`PLuIjeUe4TaJnwB!RZNboHN!o+7#crAYH}kY=Gbmuf(wJkF;1v-sAItJ{eNX>g4G-'
            'gbzMPc=l(47YV{r;ev1#sVcI&K*j^&`qV(c<3FrpmwRQ^Jv&}5NAIz>Y=!a*V{0Zo(m5QxGf-TO4gx^6>VyP3N$Y'
            'tyk^gnsB#FNiW%GUVYNVeu`POjXRxnsNm2R$8dP*@0udEv^y&1dC^-'
            '35qKqfZcjh!&dhw+iN3a9v4CXpTSD*nOJ>D+{x(b_$PE1zxCdD_~*{m7;=9LRrg04e(#_)*eW8wJsRJq+X4&w8G*'
            'YD!Eu2<M3?_zjJOdZ^aDqg!gdTf^$-'
            '1J8+t<}6N6^5Z4h1|y)gw&wku}Q|FhXAurWtDoR2gtJB5%aNzQ)<+cJ_#;8Io?TWgk6`D_;BZLGfrM!4?DZbqX!n'
            '`=E${!Ug}8I(Oy9#)Y|H;P`=SFuXHB1Ztx-`FwI_e6wQcLVL2eD~oxBVXL#i7SxQqOC-'
            '&VU0r5l&f_h=hseDduJvo;C?ZJqjn)~sukaFxj%d8)`I44W!M%tN(Sw)HM;X+{&d!b?G4O#vNrU!I&@oox6_DkX}'
            '=9?$`w%w2M>e<zpeD){T6<Q^hR5nVLWq;T6oxuvc6o^n~Td{AdwaoD*yJqaGpw@5hn(`{~T`gF6&A^+~{v@X}^f#'
            'D&#vt)`zNMSp;3eO=Y#)qn_!U(hwX~iYO3v>vvI|W;-ai17jS7y)8T2T6Y`^4__(mM1^fVd}p*alm;L1-'
            '}c5^npCnLg2X4Wj|6oaJ&hv&*ftT9JqfcWVFm9$Z7Kh>rF;Tg3PbAeYDOV@No0rqX-'
            '4_SHKW|w4D$b3(xrH)e)KDHCNw}k7ya7W0Q5H^S)Ptm0ko%O>qc+X-K|#Jpl5&7{5Z4>DgUGBc-LFB9o@D-'
            'HGyXBCbKr9)khf)`&$d8K28MDbE2{>?SdA{{cY`Vq;&poZHCi1Jw2ma?30d-'
            'O;j$=Yf<z(SE=h;6X2=12wC~O7u#)j2{|fn5pNOIm;E!z*FQ#*uedEw1y&#}6_bdBRxmQ5QJ~Gm7srtpZf30L7hv'
            '(xcFwN#{&M){<+GPR>>H{#kxsk?0B!5_fD;5jM{?{Q!NP9ZW=TzS{R^3cIR~V;a{}kjk+Zo^1{Ein^Hy1g(l?UKD'
            'Y&!5D3-aa>o&<{5)Tt$TJ@gUd5ncYCmJ7jmmJ1-'
            '7CdC~z5qT8%+SE_m#@*$xuZx?MH?x6KuY|3KRH}nw`GxOyV{&3;&`KCj4PC0!Xkw+nQG-'
            'F`)tuHiMzr^JDi7xDqNCZ1QxxjWQ%5Cge--onx+y%*uc%ztr3LvDpA8oGB+lPf~?`m0;!)kA|n`v=c}eLAzMG1;n'
            '49wBj-g4n~svJp4TwRpS?UeK6-'
            'rm>P`OU=!a(~r*Hn8AD*7RdG@EDPLGDk+cO3f|C_^)`7;z_?0i!1fk!N4Q%~vG6T4b4OF&Lf#}E@G7){h7VZpdWT'
            '|yx?wz;gYkPyHn-T0e{QCqm?$j<&7vb#ug^+p!6ipmKqW&aZJ5GIV3b<9gWsn3x-'
            '=#5>K7toC4BihhA?qg;RCbjdt3VzqzVPH9)I5f;rk`Trt55CHa)x~Cxu#Fv9;e_QO?8hRlP0E0?<S8NMicju`ig='
            'B90TyU9UD<v*Vps_w&H^-nqra-JjUwR|*fO&%V&cGhvMMSdI`%W-'
            '5`fgRFNnfp)H)1c3*PT1C*^OO61c^;@aZ$VT8^_TYRlj?Qcd`ndPIZqmw#KMhu*rH<1j3E0I`L;W&<65GhifUn$s'
            '!Hp_@^KZJ<XHt>PqAHys(H3&?&U?$`Qi(U^RbxNnKd;^VJ(pD+Ujvz#R7*IZyxePy)68UU_XjqHFN{!kESkwqF~e'
            'j7Zn^WvIyu(NWC>7?hJqK*<HCRdk~3K~H9`f#j-u`hre0K6trY-@nu69uwH$y0RtP-'
            'J3U%x34s_+10E10K8gffx=Kwkoc673q@~MAFnE{P@ZsMxypNN$*ASZUHbOnDF8)>P<~I%Um#|{RAq4n=K55_ih+C'
            'sT^Dj961XTO)FvWc#y8|DDmsX(aDebkB2XxJU<GZTd%|0vzW)1{)?Qb?CFz3m9rw7?rbLr_FbRz&Dh)n94zuBrO4'
            ')qiPizH>@0s032V4Qq;R2e%lDhWGz}IOnM`N4W3T~lcx6X61MmgOKD+f|cC8bL;;F;ypXfw_{bqp5BJam#(QtV*0'
            'Zlkodc{T4@R633;ehd#NoaY@Pni%3EkDx1@nwy4Nj@4VaYd2Fk$k7_QzT&6Sy>CTgZYVgyQ6H|4g2(<prqxeMi6b'
            '(#&8E79L)~oYIOy0%k6rDja0l*OHZ1@UW;N0*UCB|sOfdlP=dGu*r(M6>a>+tD(UjXoJNby{JdPfnjXvXo(a{2m;'
            '{!)bcgs|q+(hKB^BRye7(M`7Yrw&zA)X%X6z*mbv2Mu_c#<3nXy|^-'
            'y3&ww<BjfI245Xi0fp=)(Qww5pH3h0}I7>0_&Qluf+NB`Bfq$3i)m<V-v`1`^Mzr3#I40iMNa=TIfP8Y-'
            '+If7ReWUlDgB?v?Np4Me8LB*{S1#DI!AUuKfZ|_CV^qIr4evGI99$2=z=%w#yYsTEv>Z`i{72BlBU|slI4YT@2&U'
            'X_vX=N}{sYPF!nc(|<OC<HdpZgJQb^f`7;apoo;^g~px$O4m%W)_S^8y8!XYzz75N$%!)NIU0}BJV&-'
            'T&qW4E;*qnR{}(dGD(V'
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
