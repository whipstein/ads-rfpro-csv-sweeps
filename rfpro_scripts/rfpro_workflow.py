"""Self-contained RFPro import/run/export/geometry workflow dropdown."""

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
DEFAULT_OPERATION = "import_csv"

_OPERATIONS = (
    (
        "import_csv",
        "Import CSV parameter sweeps",
        "Select a CSV and append or synchronize independent correlated geometry "
        "conditions without starting a simulation.",
        "import_csv_parameter_sweeps.py",
    ),
    (
        "run_analysis",
        "Save and run analysis",
        "Apply the persistent FEM environment settings, save the active project, "
        "and start through RFPro's native Auto/reuse policy.",
        "run_analysis_reuse_existing.py",
    ),
    (
        "export_mdif",
        "Export analysis results to MDIF",
        "Export registered or explicitly selected raw swept S-parameter results "
        "with native, point-count, or step-size frequency sampling.",
        "export_analysis_mdif.py",
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
    'import_csv': (
        'import_csv_parameter_sweeps.py',
        '9b3413ca83d2657bdfad507a7a2aa20dc9cbfedce438cc41dea6bee22f1965d9',
        (
            'c-'
            'qB%Yjfj9lHhm#3Jm6hi8aNxcjGSR)XTZ0CG}c+>Xuqkd&1FHzz_*a*oFX_09(z`=)Ye+>XB6_kW||@H?iBMfO=$Q'
            'W@Y885^)@#J}m218_nv~DlfA(pGTK(E>?APm)8$@yV^vvtjU{bv8o@UEIPXSDOwa|J{}A%*HzTs7Y+R#6;)Hrb9j'
            '(P^)j#2Aj?(#-'
            '}$T^N72dW9LCD4?6!m{aF|v77~SSGn57xi6^<~^q31lW+UVC`FS1nz^XIFp{I_*p&GKJ=g;A#1>zgK8>bKG7tXu<'
            'lFz+f~)T?~3${(_#lIzJT`2STNRdpNXUzYGEJS?iV#`R>YHgAfoLQv;x0Cg}p`BF4(QQg59)x2nnx@xFDfC}?M-'
            '&>j~dRVs^z8y!?B?5j>SLG&JFXu386ID5^crYvTY{kd`u<OSP#|^CR45q{t!UFSUnavQBSsOjp>v9f{9_r6ItYeU'
            'OK#PC?w`D#11aPgZGH;q_o;U3ZmQp~URerlJ$~ks{hOqjwm=$fg87NAO01?sSeKETyI!CmGdERET`+WYY${(XDqk'
            '-yMBqSpOXx(Nd^af;I1Hs?7(QRF~Fl)BNX#lrCL;wyNZK5VG7Y6`u3uJ*VQFPh@SZib|jTgPF!F#|YKuBnf9*g$A'
            'UIT01XVo390GSKOG{Z&a)#qYWR}U}|40(=VXAyu^&9f4?X;5bC3f8b<JkD#R2+)6%w@8J^nP`>Ia#$lQE^2e!4%u'
            'omf~QRjWS$Rx{q_BI`u<{?UYt#@-'
            '<)5*g&!aO^YmSMF}?or*IyBRC3Aiz1_eC8qL~tisW^@Y1KLGtx>&dCRi36%!J99u05<B@3<mny>JGTA$@Sl}=Cl6'
            '!khS;vcire;&H7d$$2{3IJR@*qHY>9RajxE(N8DlwLzcy@etUs4(2I7nB<A7g(+UuC3Ve&qGm13#4hDliM<>9Lhy'
            '~!HdA`WjC2-5*y%q&PWfT}!vsJM~Y4h-'
            'a+j2%LhuItCth+Umvl$PLPu@&FoL#3NCJ4#VBm(T|r_*=Sv!Aa{uhMtZw<qqa)3+Drm)Ggr^J99EHJ{=r`ZNC+MX'
            '}mj@UvdQL)x{r^VRgHll0>9{J&0)uA%q!YMsNfjtc;)0n*UkdVpmWKxAMnA~x(gkRv$>H^z|>pjJk~wgYCuG3?TQ'
            'nx1_)Nw1EkX9(%{<L?lID9nTiZXWY|sU@5vfeK{W1&BOAK5Y8}Q4PC=IAdHiv$AgTVPa={JH0;oF}*xFORvw*PA;'
            'eKj?}FA!T<6aO@FxRHv0a50C-'
            'ohciv<r&=*A~Ay2K`7wcx{61>DeE#XP;^FON<^4S8!fR{DOaO{o(gtik5H;%6Hh=KoW)=Pz6l2On^f$&hzbGy>xl'
            'j9E;XQxNg>yz|odUbMTDLM5dBg<J}K^P2>T%g>>T@NH?0X2%68X;c+n-?ntblDyhf{4?zv-'
            '7{flvmf6AC9h1fqgDdKu8eY2vdUrJh?i#{ORO4Jvu-8@b(?T^Ax8kt~^bVDd9Kl24H;sr@|)u`8-'
            'J9OwX=Pm|M8(ci3owgX52?#((R@0{=5F8tRGt03xRwzW*No0R&LbP2Nz~3jbA8LdU`2Ka6M?f&}<`UQG~x$$%b3S'
            'ICn`0Q}(~g8zY3JFjwi+G@Sw!16zxEF?|voL5XTCV_}!H1&El%TsuEh(`xKE3@0YJOqKhqCd@8&0*B8mu3Eu|AqG'
            '>Y;-'
            'e<#^dn~wN==p&MY1FThrA~$I!?u>jH)ETyf~KTsQjo!E^8+d&K>SOPST>`k}&84xZx{H|wIV8eW4p0jXJ4TETx!Q'
            '(Ba1RNPf~3Z*<xPa~2MX*0{p{4iRSb=K})w36Md|6P<>WtKjT%3_hvHlVy5G}!`H4R84%C9MWeP|!Mn=Jg|>$S5U'
            '^8nUrCz|CpN2%6!Fjyd~?btzcg8cC+fpDhq8{zKaDshLHif(|8v3bn6kL+xw|n|z*X_&f8>=Y)6X;e5?UJb>JM_F'
            'uB1);}T%^z<=n^d3J%#i`_hb1^h?j(MjPymXakjY6K{Y<&A4z?6X4cB95w==MWYy^`qQuQU>qm%#+}qoRk@WbBTg'
            '^bKp!nUYGja{?OM&>ThflRk9mFecR$WlnfHtzV}~{_dI%H3_*KQv8Re6%hbmcb0(%km=l^kr^P_xu@Q@pyRZlFj('
            'QJ)n))?USzPBfiY%H^eG1|2+kZhh!%MK-SgpIf;3P^qrscqOhUapL{*H1$Oa9s6pgS$*4yZ5xdxS4JdOSly+gg&8'
            ';2G;1G={kGYajRT4-HZH5m+$KEUS79F^Pjw>E`M*TPC3Ql5E8WCA{AOcV=LM#s9*7!>tY+n|~-'
            'jLV{0e~FV0IpM|aZ(nA&<ED;7gG3Y90*^)YZ~q#1`~C(m=AcT9=VjU7d!DVJT^yczR?q5eJm0`?9$}RgaE>VopMd'
            'aN4Hxl;$|@#c2kGGtqbE7rbDU_T0dL|K51_0=Nx~uiu#&m?gtH*aa3?rP!SEU(1L1zlR$$1HCBjP1^!V!4$y;P6Y'
            'G+xAPUDNs6-@X)$M4%Cv}cu${~rGk=Fup6e^%V0O>|l<>Vaf0Jhng(ZD$1D&#-'
            '@Iz(NJewGyP`M_ktpbpCiVFgqS3ZmL^uhG>%rL?HWGN`Z!P=xl9Z(YgfT3qxYZF<bf|;8&mstCtEG;_xps+=Ay<L'
            '`Z)q<O1^uIL8c*Vgj%(m*aF5FUBnDhPrR!u2Z29>9T#LU8E!uG+HbX;!nWQ8v9M`!qpuldL>&c;D~+*SCdkki9`D'
            '_J{vku)NcfRe8D|041@rkH=w&Ji3033^jaqhDrEPPCt|RG0zQ|HOAARe6w(BMkbS#o=|CZyYY^1l#74+qcBhWfAh'
            'QaCM6&2YxTb~0KHhhBeBZ{~`Wp;MnN9ovSQ^G#To-'
            'r<!)y6O;Ejhw2Ox}7H)A#Y_%3gU{!}nfoQxYFMmvP2h`1(SCN8dl5Hz0qw3iChR&szrQ11p5haM2gwtpq%m9uwj2'
            'e6vyzr!RX3uH?LQC60>+3XWR+@Ks2WE;_59?}T_c6#w8VTCjQlFvY?xh42a6Z_N`RJiO6H5FI}uG+R#Y}Yt^uA7o'
            'L7?+@&gY2V&u7y+E7YXhPw6ro~@C1p|<rWl$PxRz|nFFK?<XTvY#~$&I7bhoI=Wo*E)63Y10?|cqSr7<9jcA|nAo'
            '&C6i0OSzhmJod9CMfFKc2rmu`}BCdrfGYYqsM96%}J_+&#E7jcBU^ecZwKIIOfl!T<c86ARs|phh{&jYpL;53)EQ'
            '6IcR4b|5G!f34excN_aB9X(C@SC1%r$lBRG`>`a5tGlwk9g6Lmbj1a%je7TOS#Rr7+m~UH&G-'
            'A9tO%eq=&}0Dl%TO5rVb<_k#1yvAZv@rS%ASaTdx{W%Ro8A#XiRl^SC%wYE#~3MTz1i{-'
            'pv9aQxpjs8nj?1TmqZ%+W6w534#NSC-ZVd8}Uj)ozPeD6d+#d=iWO)9N__OMtj)0ah(oSL?P0+`{==mYeY}RV)Tm'
            'nk6h$9F@<%R99+^hq#(2wYq27H%2dULtf(Mm9m&nTOKbr?BYc2Hva<pt+JCa*suaA3;&LJ7^7-'
            'yr(Q}XhEcP9)5z1g)Yf^ay)x*qx^g8>glB%dT34<``Y|r&XbuyLS;&%`k;|G$<_Y-'
            '}y%*V%VhQ!SU9MZQM%@N2@SpcsNmFMhL_piz-'
            '4a22=ZGRwtOhrz^|RIE@Cy+eXiwvT>BH6r{Y8VXE1|4^H1h#sbHFr^UPwLG{VLXG7^Bc;j^5>OBl|ZDt`rb#+zcH'
            'RIW|li<1pBQUf*bXTY&89!&}d`Ot#_46?gG_y=NQ@jiTGNaW2o5mRcxR|3lF<MRn(Hl-Th_Adj=@p4O|BoLT8_!n'
            'S7{yz7&=#Fo5!4(i8>3|ESX@L+29nOD5+GI(4sa|}kZq_ei9!}L0U!~#Gv+6ny!9YK4snu9_uP(Va$_PfnZz-'
            '1hnSTw_~gfWK+SWLtoNnp9OE)1RA0%<UOaj|Ld$xme@%7~_Va<w!Ng=0Yp$=xB_`ftS?6ciJ9laa@P@4?Y(q3)g1'
            '(=_$<0U2nVI75ypI15VL(5OLPR1#O@TA1pfG@LTbr1dYr8&Ss*$2LY0yS@fp)q6iD2LrfUN~<Ye<U?Y2d_GUDzo('
            '-ydZtm#R*X`c%}DndYE2+ovJH$uK2v|7<I^h`<mZ?aEC1!+razxe-yNr>QQ|9Uat8Dhc41duhbIj50Eg!}1#KRRs'
            '(8rC_}SAfckCtFPw(nT0faDnFd~;^pF!e~rGgUpZj~+X@ucV7H1@U=4S7ZpcbzC=do&#SeC=*f9gv67XL)4S#nC)'
            '>bVdKqARLwHwAHGm#^|(cay)!ZH^+=+rd{Qqi+bI3c|&(%TG^K$^$Roryd&GOm>ikdzgveNZ<M81P_l$$&Z#xH)a'
            '`-AECsDv^V@EAr5{?v;@^EEkC*k*pn&(hqJj1U!;F@x`f!Jqr-Vz>gg`N5QM~PuCK<d?FbP7iV6q7uMjzCH)mdJa'
            'LkgKuC}o7<$h2BN+~zBa)p#L>3br7~sK3*)shieP9AQDb*|dZu$rx-$*iuY7+)ajjJN-'
            'DUZ1?$32v0|u*MayayE0J7L})pBST}TrB5%|Sv7aeG{A$4xev>z^sv4Ao>J@BJQWCy@^_{0@YXLq_MHo`!cUo--o'
            'fMQ5DhMqmL%uIS<(NB376AQ0TOaVjP2-'
            '5Xiypm$CI$M?JUqFh<_@nnOUBbk;4JCYMM8MBxMiStPK`;k7{<3!9jN6NjX|6PDtUuP8Ped%7O?su;So9jID3kEb'
            'O=bca@y8qz9JpM5^*F#^8ExwZnCpiRes0WV<xnDz;?fxp@*90{r?+^F5)Lz&2xZw0%|7YINpz72IhnlTJ#G3J^F6'
            '^-5&^yq@tNcQIe>datPCA9S!YICGfiW0&ctxLroxRF{jSmn#^dN@rGmOtIrtu&#H~mvnd(r6>2T(G7~u-'
            'YI|;x75qD~`3&lawZJEibyzI)sFbACk(4xsMAjl6@@{xe{^g0f!nTMN=D_rsE5u=7AH%#um879#Gi*Q`#VGBhZ|K'
            'B0^cUTzfGaG5bmpEk4NkBc4G8_gJd{fSOy<{cLdqJAL(YV{hX(M6RN1uEWAU#zcF7#uahowyzJaIj>h=wqs#3;~R'
            '&O*mN^U^U4vh7z*ztwrwUA0Z!o;Vw-O`6?RBW8aq)|K}vsk~J4uSNJ@;ngACE0?69n4-H#w$>;^J-'
            'QjW+(BwT^#)7pegR)X_Y^s17QNT0*V@#G|wI+^JViKed54H<Ktr1Uebdhw@cihBEA_fioBdV>k8@f9l?K3&N!kzr'
            '_BkHSmTA>Qh0)Y>K#N5dF~p}5($C&b=3v*#*I2`hGfQYd$+3sAlb2`m@}y;M;MbO&~@K#bZ!-'
            'eGh&N7bDH478gc;)pNQU)@OtfLrOlYqaTJgIHTwS9A%`7xFZ>&5O~1&bXgz&1ioRioksUR87EACsTKd6A=ai8u?F'
            'aK#=114)wNj@$X@_puvtl0#Ay(SaX&NV;mO~*}m_eh^{<0kfd$`GKfA}(eG}6NMLc@)3h5ORnpSFX9ZqOmj)^w^X'
            'ZiztRmw5&c5Q~1EFk@-'
            '#lfVctbmgM;JJQ}r#ru{7q<UZ!04z4wh}M+ojNy@}e}wINF`ZVPT%uEn6h1tx@_E6bPv>fgNbL-'
            'H6&CS{?k00UpIoFokE2swhTVgqv7RIrp2Kbi{2yk0Ysrn;1MPFV+OjI{&{79`vj&yq7LH%gg<x|pvsr$yq>RCc<R'
            'r0SGqy&u>Y3hdQj)<-GAHLS&+zXckrlI#y24gCj8tAAg&|Essfb0|c%-)aV7%-RQ)?-'
            'F49_sBEFbbD7<GWXKl#^gr2ZY>$kDy`;Pqe#E^LWf+4+EZN9GDo#%bT`r0NpT-'
            '4{6OBzo$!(%3zWh6;LeOIXsy?5LxZ1uxnlk*LQR8QPJbB0$G6aKJ<34fEWQTXjokB?81t9wvdvWhd6EgBUU~oJa%'
            'f*Mi)2ZNQt4PV*b-;@CE)^M-'
            '*`?B?ZLdraqx?ybU9D)<O0Hn|B!d2wZIfrjI|d$Hg)hlmxuPddh_#234H0z$;dI=;{*FRf9UySCwUHs?4zL=swWJ'
            'R-vWvzKi3F20wub=l`CgC7}<7Yo)C#^)#|3-Zt&Y>dN~tpAtFB7nB&FRTCG7*Xo}-pk-kqcb9goE_C;mQ!2xHc1k'
            '9_mNM4cL)a(<ed?gV2c=D9>~?iUTnCrpmZQL2S^xY_EyG394Eo11nPwT4L7hy_k`pKue?dZt<?pNiCnq7ArlAsC8'
            '48Si4Z<D2m9*tu>19WCcc2BPF=^~RW1c-u@Bv2TCJ3R3xGYzs9JeXMSD*@Q|*1F&9)b|_JsZ&Ilfxg&GAq7aCn-F'
            'adI5tMX|QHEy@DSzQ+~v>`EcoI6CP54d2S~#jeO~R+Pb+hK^P4dv|czqyEJ@PO@Z7vpA^CKnvJ3MZ?X9N}shJZ(1'
            'wj=}^M;G3=$#7o~YnSPu`H+^EU4@|>!MKD0Zhw?0}<p24dJ2OS+;IFn}RWW~$QjCd7mUv&^|4LY;3K~N=7D-'
            '`;^TBDPZ*=<!c+5{My84{Jh!N`I0XP#<uIG7mG^wwz&k5o)YS>0hGCQ^KO8cZO(8eiLtd)K&;LdB5QCMXhcgC5&9'
            'pgHY6>=yA<t;n8cuIFwXO^qe1L2^76EP<YV<H%2l^%(YJhl6pCeqnN%M4K|#<CE9+aObGs-GpOZuuMZc#bS+3rJ-'
            'xb;<_Gbbt;6EJA`lpAbjyE&F+w9t=?-MN2%jL-'
            '=7oW%u6JrEk_XXo*VU;z~ZJP8;$nDkMNT|Z5JHfZS|~nDS+9uWNca=8L6sRC4p-@sPRTosvnB+cpR0FWF2mH-~-'
            '<WgbA7|eQD3AT5NApHl|iXpPvA1`{-'
            'NY!BBH0UVa<8Ff_gm)C1{xau8|Pqa8w9MUfSBLRgpyU$kyJfh|*^0arJnm2feP=x$Dl3;{&a$rhsvcjD+UH{n$7^'
            'Fuvfm-'
            '&8tPUj0WwCBqYIC_+UUEtM>aO!2KIu1I?#q44cE3&sX%_MHVwZpzL>4!T)W4WGjQ(!QPvZFeMH@s9s_gEc8Dv%Y}'
            '7OrGwO|gI8D_D1#+u5<X=P;ll>;&)lZj}pAphJ_lX4s$Dt)PJRhF1&L_5k%xI=D0Tf_~sejdd%NQlU#07+y-'
            '1Z^I!avlQ!q=<;Gm0{aw5OXOR*TBUS@U&t==dPc<|Fw@yoNl=a>bF*Brompv5rT{J+&wf%7-'
            'DPeMEq9J96NJ(^!!&fb*}$d*A8yA12<m6U>daV}9`22;?%v_407g>Q!hfj=NCJn4V(IYmo!&HvBLoS)&<z+T;MTp'
            '+kUc8G15CZ}Fn@afZKtdKgJV>fTu$=VzDPJqWgi5bRxlD9N-}wX@X5Xf<=IpN`j-QSQ-Hp>UALMCcCkYrnxqe_(Y'
            'K6YMMF1pAOxNQZTB2ZGIpZr{G>+iS#F>=thY@$<AXPAnJ;#+=0Aj~w<_-'
            'LU(_B0*swosdWo_SmDPFM!1>>XUVHgiq(?4V8H^%W<O6Il{*-T!js7&@_v-'
            'I0DOFYx!v2~oF=ZTwQ(j)tA4e6ui+_6FOr`UR;RqglCVPkJYyp!lWMChsu~YM<V-'
            'VPxyG|1ULEvRxA}J<avUS@6?Wk>+hND5hmu8{pq#%&sAkHx=BJk$C7khRW>SVqh?*Xi45m16sHgWaA)uO7>sDq2W'
            'I@O%51fif9hX^VuBe&$m4z>r5*;1Zo$EN6XcFOjQwpEl6T|32c)U0J$Kc=EsPO6G(bOz`xfTJ^7`iqR<A9$+(>x-'
            'yLK6Kkr6e+_iM)&oK5+ebo11v|Tszx}OEr@ZOBW;U3>0%SlTb+L&s!tV`1k=T}h<s1@A50H&Tmc=7QUHdg$II7hy'
            '1kYEW2)DK8nMkGFyYdjC67EKApU^S2Y500hFg8Jt4xzjN$g=&C#A<v4is{<BO+jNUdo?tWOLSHVLo*keZQ##5~n-'
            '0Zq%JxDSfJbjZq1C?^|75v#}C8MiLk;G9VigXKZ^)eB7clhZF%l0-'
            'q_`EtfjMxjoKcVL_QO>^g#$RyJ4F4})*r(m4f;L;?|z_pzv2%8$?6VbWh{2U>jBS5k-'
            'G33E@u$!3@VS~%P_`VE@5VA-'
            '^G(|>|{8w0k^Hru8^xv>`)r0$`qQ{#IZ?0NFO@Wl0|C8^>vRo~GXqSLpN==;I;P_mY24zuK6RM=oE2@ZWlr)Qul|'
            'I&6z5RPk6pK!7QU9yL_qsZdM=1h27ISG%x;34#J6x=1jp2%(cGS~i0=9)$Q@Au)geR-'
            '}wI2s7tS^J>dO<(j5&^&mLtye6KL6i-'
            '9hVqQjprmrRynA!T2ukfc2}qcL(A}rC8&3A=tqw4^d>2;+ld93g>LzR(Rl^{f$SIF+^$Q^YY#A>xSh28cSGl8AT`'
            'yyK^T{dMX6$m)O$HYBDcpt`!vasXPF&=H9(_xH2PX<uX*0)>OW)qc?qmmBu(}1>09Pd2kmm-'
            '=`t@}8VwWVHuDa%NeE{{AR@;CK+#{3IDc0O?I?o~6Ve3G~;ianL=@d#vm4Pa|iPD4|$rlBkLEHu|F`7Ekw&<rQp^'
            'TnL<zx(2a1P#!yylYF3MW`YLD#2KesR1!VQWdF8n3i=D*qB15*2tV$4GVouy_+K>jF#XM%T4hei>$_JEWOY{WLJB'
            'TIUG$w%rCEl@y4`W8O5O;SLUnJrBgJ2a52oEnQ@}RS@<YOr0ugz+^BtQ)gXttV+unWC7tnqps+hm|ym#tUoz%_Vg'
            '&UZztmSsCTDM{0F1$Qf?A_Dmw*ErAhGVNLJX=<trzyBpeO4sC1LSv(XN5I0-'
            ')<xjuJURB@t;Pj)OVY<R+LB%Hox$o)HyMHg3kOx!=+q?j324Bs~_*5~}`35p$YO$A+2ot**ALAzPz5ta&CFHL-mY'
            'Q^(yDqSfa#}fr*5zhXom~~{a5^KU?jv8wXRAE1roX7JuQL|1cU|W3UtFG_ud#PO(Cuyo|+1%@#2U(mpdUEjudcya'
            'eRB-'
            '>opA(HS_~i^a6QL0}CKPz)Qz&2~M%XWIga3oxfmn+>)Lkbk80(ANfh1cK2BK^^6>+iCBz@`M+v)K;X)@|bLtVs-'
            '@h3ry5D~j3NU->vAGy+Af|$@Yt>$l5H6Ez*4^`26l-'
            'Q%P$sd9+9q7c8d>!2NVJVE$ZnkR(Z6W@5qHC1KCPHX8WcfCx_=tTq;^Zr`4nBsG^>;+)oGv$mz7+B1_n`b_PlgPn'
            '3Wu>D%QW%^9kH60JDHRZqdy>@Kn&E$D(K`A$i{(;f_S9TOBA^SGZ`Dzj+D3uOye|h@(TF9POQY6$Nd2sEQ?b0Mrr'
            'WnVL(IVw|wGC^U|cZsPlA~sL%!5ouEtOCsNuQ?_RY2!ofV(-'
            '(jFM)yFDd9oVl4h}!5Xr?qhc7YMAbR=qXDP&PDGy5%6k=n4fQq<TPEW7wxtPu<HG>Ggt#Q$+GI42-'
            'ro5B;F1PYjBT@=9e<_?H*AISzd0!I*QIEwpWvGKNI!VPUf{AbC;2q3=iBD&;MokNeUlyK2%F{L)~<uJ5)(!m!VzD'
            '`j6w%f7=+&6frax!~dY(nW?A+S#+=>k419#NK7rs*dOHJj{cfxX6l96{n}nCe4H_@)axg9qLZ~Gh3DY$%Xj2_egg'
            'L_{Z!lUe9ZlZ>!4v@M7p{kaD;LcGY9PvWsB&3^r!<5^HD&_44i_bjl{~iS9=h23wd!*qi!GF;3ZEPa2Js=(Jt{b!'
            'e$?Vg;?pz**I6MvlZMGq#>Xr#zu^6~a2xkh@GyHPhr3)tItdi=c1*$$@kwV%ht-Gtep>*czIx)C>w2U!Vje$&01O'
            'i#drGKH9x*m8Uhkud(oH&#eZNtepP7`wi|mIyj&*^#47Sp&z_!;RBTHRS5C4TCUsUA}i}Vo%qW+!6SS7Wa2c#>tL'
            '{39^9HCBT+n-'
            'QpV9eYBX5BqXp)#ZKbbB9Eyj0=g0i{o&70_t~$ve8piEcL(Fvy^MN380ngA%qEG0#7s`6ji)NC>PU7<jy6LDg|E#'
            'VS#oZb&hVh*)%@+0>5|~oywel%^5g01zD^9%+ow2M;n9M2C*S<#bp2KFNIy69!UNT?N2>ypE`OE?0OIpj{x|U574'
            'gX~fSW8~No`M9`kCHe*Wex0hD&xre5tysKYf|>2)giF5dr%Y(y<<es$($RVQcjmVu0A(k>7*c=Xr(=n@=J@|#C(@'
            '|NHXtnP$&z}?btWopVU|TzT%+qhT=2ltK<-%y-'
            '*RUfgfpl)oiNS{i?2tzteZ{kn%$vzEG)K)}nEwj!JUFkPT+C(UliUG#SES^*LZ*G!Zaay+(b=<;{PRp!6%>T??*='
            'X6qG}yTk%i!0u1G&b4Q?J-'
            'wtgz0_fojDM+)h~K08`Vmp9=%c;_s4jbmoHYxmBA9*f{U0U1*@19Cyt&^7H@krflu5abYK(&P<99bIUamhvsdhXm'
            'YxyG;C}H$#gi9ZXcVV~xrcN*;wf~N8;KH#OmhSwrhs0KTPWv1#{_S8_Dh28vIXAMzRWwAFxOa2o=GEzF`p~ODopw'
            '}r>3$GxWGabUP>h0RS_oR-'
            '+tn_uH4#@mc7rHQiLZf><6c2knH%}JETWeHm&&F)^_lEdQmnV5@qom67BYe^&zsBf^7&h<|93jbvXzIbMrCSB@(D'
            'Sm%le4>f%5j-x6yD*B_l+mSAfcVCIQPEB@(I=H&sB`XHPB$-'
            'NjsLG6(v3EZ}xL^{=oWvJhp;I7qnYz4{og8(^;6_At?5H#cutgDSA;<XGqrgT5BGuBcCrADji<iM$Z}W#?DTC#r@'
            'M`#yTf?VX6N>x&`k9G_lIe>giie%<?ZS)Q0hr<^cxz9rD;Pj9#%TnNMsQC?xOd+~kBCkeHAF3DoMA9u31k?&p9hI'
            '_s>#j(tXy-6d`IPEKAC149?0fc9J2U-'
            'V@kD1}~xwlG@FtBT#iWFegd{VWRoRI=41mO`+x+)KV#@PgWtv!@>5T42yVmj5vTo?C%?|gRBAMa)mOjQgrOpgcLv'
            'S?p*miTYe%Xg>m{_`;OId`eLn;j}H-'
            'UfVa#sQ))<=XA5KL4nEMtkPtcrm!Gd;BZc9lR5vzj6Fp)v>UxLf?6y5xuN0I30PthKUIkpeEK*s%%@aqhk2so6Z{'
            'JAI{E?{?ExV3-'
            '3T*C!*tajg#=D=Z}Yfxj7tk!m{>cfSp1|^+c7tjfHAuqO9JPW?y_NAYdqJ$W@B<aovc!F+vadYxI}HzG24WF;PIA'
            'bJ0QcmuD^mM-Mz*`j<*Aheon?F`9a-'
            '2Yq7;m1S%B+KYla?7p{o(`0w~5A_#SZJ~lA980%~H)C>ZVX>w@OG^7;{bG)s1M<Ix>_9N>UviSG7SNKd=0B|4wyw'
            'rM11<ltt--r`uW@uU2d8?KlN}Hkiv%m~q}l3@?q4@U`1RR03LI6Rhybmq;~4!oR2|Xi{SD#RG?=Q9>3iEE<^W=kJ'
            '{5s^d&&%xWsp7Jk1Aw=1jnz&OHB)l>$jw1<2QOIor#b0MFujj`7tk-'
            'Z**gcIEERIM}vl8d~g6q8*H~Z_nzp4Ntm5JLotf(VZ2FPpiv%inTPg1?jLa=Gbhzq6&Qc|ZhH3f)#+9GZu<5_Ptw'
            '9Dx%P)SWl`cC>yWderXF{U>dBBCGNUNq=5aFgTsTkPUYuWEr*F@XPe!5~F+vN&nF`e-'
            '6GrNKKj?D<%2(AX_!N&`urjhN<WAfy^NF~799jT<e<8g(nx1tQ;Fd(UpC;fBeE@TU4#TRe{z8$E3nV;W1U(&p2f+'
            '9TZC$=_6}>l0?P|Ig^Xv!uNHsN@zn4w@S>=_zcq!R!^VLfU+;bJ2r7!yFq>TIk>(TeE?5mfdGMmjcL&=eReS^goM'
            'K)9VmPRZW*0jJxzLpgCFTLlUu35Nev~9ceX);$Z3xd;42|<>)o`;Tw3d>jgyb)%|8`bHxypc+-'
            '&5nQWMHuboiuYm_KU1;=Wm|40dpv_P8!1HA$E_)3W6csODdkyd8HKOO1bGqrRP{lVecpR%3@7`DyTyPI^~D0E4t`'
            'B;UE#<t17}0Yp&<~=8OAD(W*z=oJ*i-'
            '9<jl$G?A+(o`oai6VsHIK1Hu{wJw$+5rAX|z_~?!JsxL4p9Ju5OLfjKWzAEW!Qz&!wOv*Q6ztl(LB(CzK8(V)X43'
            '6I^Q=gh_i&-;VsSoDa4-a{jy(rJCxi2t7FV^PM?M8jviaft+jIsD)5#=Q4*6iwF<DK;uT30N-'
            'rsjBKDBn_z>3kbaeo&zMzTbBUjE_|jH(=gna|WLvc&$GjN*^{wB;!q*xuZxBMer-'
            '1^u0X$WxPZGQ+e7(us!%QexMM30?iYBWEy7iolvh+_sgV*`a_Canu@Un4b11`D886<`ipOK!2pKNfqBF?u$@F4HK'
            '+VUHqu=;c{WAo9x~w4{j_Pzd4_@UigQRcPxN=(6(IN}iml&><d5(L_kkTn1=9YkR7}826A(qOmA*q-117FUc$-'
            'RpCx%OWw^(z$&Br2yz-`rc1eH)znXhA>;DVnz@eo8nPm;vQqG_z(shj&MR4zK3=(+8Kp<&Y;YlUKQm%i`A$YHI_-'
            'nU+-'
            'Te&sx?Gy_Y7b2B{olhZMf<Qqv7OwsM>Kdw2Z;4xc4L^3cy<D8rPsFGNa%JRtODIJW4BIAtfGL{nRkcO(M`)UEwX='
            '~QlX0((?NNck*_C5%rfTQBpbCZ;(EQ4IRUMuel)&)jwF7q4(@>+{3#cPmUqi(-Nn&-'
            'vo04RsEgQ;%AxJH=1;hply!B#2qfl6G)H&`H=*eIoAK(i;Pre`LF{84_F0s2e<&|#EW{gM$)_31LzqMMyXwX;G)d'
            '`OqB5(9}Rq#6lp65*?rK_zehm8)Bb9$)fpwQnFS1N}5@QDH_n6&TcMg4d8+{h9MEYC*^QuBrJ-'
            'O<;&{$1T`C?l^rGmrwo=o#Dl`orGhuEW?Nv^ohU_n2p#qAk%IxbDPB2C|few!^NbV0v9#p8wa$(Y4dSWwNTK$=oy'
            'z0fl5RF3XBfr&2r6*=WuB;UQbOu}siB`2*~^<9&X1{7N<<hb~@gE|uT4cjMrAc`CY8p}J^~sGM~@$Uz;eatKVuS9'
            'kk^b0Zygb79*RffKP3Wxw-emA*K?WxSq9Ti0uci9F6Q=R0GnZhM=LBtz-ENuE&|exi-'
            'y^)k^tB};b3^t?%x+DXPUS}~UMpyfM|v1WIX)S~a^m>7{fCKUH2UlV|kM?g`r;~I5z{^<7BoUO>rI~c&uNlD90Q<'
            '6bxil#=Is`w+>9m(MT0zYr7NB'
        ),
    ),
    'run_analysis': (
        'run_analysis_reuse_existing.py',
        '34be888f64e10ffc21f27e24d5e829c6b55b97194b050d4abd5486d6c7b9c6f2',
        (
            'c-'
            'qxGX>;31cHj9cdXW!9*3z(dwvrEYl!R+jV^(y~qU?#+qr!khQ^FbqXdIHbTK)IDqfY>o<(*_xnc6CgK=<o+U;VH_'
            '5X|m(S-MW^Y%i+#R*E=JMA_u<uedl~lm+||XZtFx#9dn7h;@-~((9&-'
            'SD6&0teUKbf0{~$gTdtutg6;!x~m2JmFBg~>$HIV2wd*sGOnfAl*LxmH&VP=eiZ3;SCq9ZLouhn()?OfcT(;K>$s'
            'AY$mOjpMHV;t`UZZ+qDr?-79-S9TmYIip1DZ@nKZA`L@K0<9FDxZk+?t(3<>bRQpU+%)P-'
            '0{@wJhSOhR!9*u?8P1@d=g@fW!!{E;0AV7Qe@3Wx*1mE07i93b+$W(8~$zy1omnkw+W{wk)6Ic{A8$q0CMpH@iI3'
            'zt*0pvdd8z(s@AUcdo0G4whsR&geZ9THeEVpY76B9WUI0qg*fEN_7oMCT8{p&0QVOq;rR$>5n=Vpjlydt^%uB#UA'
            'Lyvsl!Ku6rvH$|EL6}epigYU`|1hbMi@oid^;ow4kZPF5m-'
            '<9bt%ItV{DrA0}mPNh=5VWZTZi7ThVBHQ>2v!4Aku@v<VB}g>)qr^>s%EuKs|v_s4U^kA%|R(@0k3HrP*x+B`1iU'
            'gOFV}`fg;exsu;x89%utJilzcWlwu_CDg%^I=WZkrgFv>S+Fr^U&Z=;Y6vbT*>u%B=95qPm%Br{3EWyG+Jej+!C?'
            'ZQYa=l+?pzA>p3<jjhQM765rj${nlo|HrMNNRJ!9YJNuR;AQsec!h{tFnRS*4%sD+Zm!b-'
            'd2v3JpQMGmm)1F0OB~bfw=e;3vPR_d67>dOpqfWAO%b66qR?QxF)u9g8K%S>|gw7!3YN%o65XWwfng3(}f~=C)+('
            'UKiUfvS&@S0vZ)+!gYhnQH6uIv*YQ9lgns&Ha+>YoG+uZ>FG=y31FIjbus&}oJF($nlCTsXFtKuB|Kfin#;10fX#'
            'n`4`AcQ2dG*bFqh(v)T4^GQj12*7&QMSIj3^VLPXvOc$xq-qNA!~b}(^nrEa{@Pao#&;ZP~qkdy_XlEV3DVU{$+9'
            '*({^2ih*@A7_f7#retn%_mKUA@;*rG&}n^zc@cTot<66>xY4W{{pb9`JZPO(a+P5GeF?&EP8i-G5_=V+2!;kI-'
            'b6{JiiDgB6t=4b1*)%<Kyh&a{k6!|6};dSszVLex80>M$7XP!1MepI-Z}+mY31#Z21mX7db3`1ReMfqg_K_%U@-'
            'Fgj9?M^hms~K>_M?D<=e*jDAh5o}hx!!`&WzaD@JN!rDkrv*tR@ou}e&;;hJJ8%}f=SJ4_AbS;yKSQSM^D;&o|E6'
            '`DZOVLXP15j5H$@?AnZJ9)0>u3jd3~pr`@yWxHc=2x_{*p0IH)vv^UKEmER4DslkfnKZAB=b*{s+#ZDRTiYR$uSe'
            'tFS79J|N-<wEHg2|M+9j-'
            'TM_@B*k47CRuiPcM_MdF6cjcU95{ZO!n|MLnz}EG*n4sR+dFM+yo!;s@YLMO+Z{igP({8_q4}gq?wi#z<JrnvW_H'
            ')hxi902o7*seZf=EfAc0$7DZi+(VWn=$0bCe+J@HY+vUsIDOoG73(1EfEV9AHehCNuOZdKigYiOnuJ`z3YE@(`-'
            'k+qaGA{S?d{Ycu^~%vH9DPF(XhQ<AZ4D}v%4z~my{bPWU01OA^A&?c=EO-7>6QB-dJ~5csJ>QGb-'
            'A}cSacMS5&(%CL%<2#CHRzbI11HEg$!x<{aS)oJztU_+n`Vj%p=eo0~}p1aNQ-'
            'x+v>as!OUcy4E5fTPp4ub%H?TFyG$9ms1dOwh~I%mYwlNpk5?Cnc<HWI$dUXIuPUN7N1p6Md^Yr+sJ{{QaKSql21'
            'CHE1<<F;WdZIQwpNcA3~GDE=P*_vfVPr`nMI@;I?e=eaQAk((m}#qK2m&9riqJCzpSAGOE7C1^zhi(LaZjbf;QW~'
            'x$%7+d}}{4$o1Hy4Zx&f@cuG-znDgglj-I0`Nb*x@!_ZWS+tm5z6-_zU%O8nwlPRBGK5o9p#mRX%X-'
            '*83IGM8umV}sLs*J@gUVy%vl`?;@cgF-g+OaH_YoPxpM&P-gglUuUH{VcR-Wb94Pjc*zr#_VCvaCPj3BXF#p^GGa'
            'fM#Yk=mFnc}V`hl$-'
            'Q^bj3mSUalL?bC2v2`?T$*kn9*zMGU=2wOy&SuJY7eFC}LXLf(d+kHTCHF}v*$d<wL$GBEgnk+)?9X~GwJa<h|w='
            '?0Y+NNK4@@NO}iEzggmxATj@I09#jqh-BF5Nn+E$_>aZB<;~nK_RDoCIq>Q^LOW`Gkc<4|EvS;a;<h8P9dt%;%?Z'
            '|G9pU_`S`$}5vsI5!GC^Byu!*Bk|<BPF;IEupo#-'
            'CK_w7n4}&ys)A}@ce{nm`(bLgk>XBtoFRaOr`zV%Jj1L`i9d+FW&_=rtnQY5+Y3=uMk)8s5>o1f|e1<GmM@$zr&c'
            'akYay-(NyC1|_BXc$Zyl=`1k}^mQk=Vz;Qy!nEDrv$hIz#so{E|cd7yhMygi1jkAtyAJGK0)C80Lkzjk7e-'
            'nIOYDn7vxF2%OYaXO<5RvA-'
            ')H1=IngRhy!LGBk$L468nDyX?bX^1uP6@=74oiIk7O<V!{41gUvY)IGX;11xyComIU|()c<rD$JF`-'
            'JUB&%x&d8WVfma#fDc2UKaaV48|nd#0gBbslYHvcDpcYWn9X1zPDN#bW~lnpN^bvLs&NX(9^lkL6#&CiAlvQW}~a'
            'IubL?4qvIH)+<Fo3s1Z^$^{%O@cJvq2pnt8$%A0zYAV9X#H;LYA=S|UMIti{Y=jWQo(-'
            '#sp$e!Rq;ls5C{UYE^?xgCU&3V9B37iJeJ6?}dznrrf<|wR5fL!r=VSfW~m4M*lYUm}%fl=B3!QcvdeWm4X5wg_x'
            'o1R@cdWuiJy9?fHoAEd_7OMtbv}*ft)|smI9`)_=Yu``;M}(~7T)0O?8BzBn`s!5nT!FVb2vGlBP@jdY=LL4=uxu'
            'S;OkiNj`phdfyBHo9JBdw1_H?$A^psvV#n=J3iZ-'
            'Kvs2BMhRr6S=9SXQ;t$r(Au42pAG^JG|oKeguRb)32v_t~rn#R)#M3Vt&i+z0q=s6x`Oh-NVSsJ*)(2<0z-'
            'F=ny&uIb)ifJakcWRbFyMLq8LcKepr%}|-'
            '2OKG5h31w)*m}k!ZfMdVcX7%d+^;WHpfs8?jNRJbL2pbO$AbNk;6~M;n|eR5#lZ-'
            'E+e?qWzkyWAjN1{m+0#iFTa{73MU2Xt4WyeGlP2&i@g87c?`zlw^me`kAfE!ttJ*Jro_;!+p1qCCqES0Xb5FqbZW'
            'njea(D=e%?1=)${dm1rg^%Jv*59nT7JWn$ehj!p%6lxTR5VU#JAvZs8B%%d|k%78w~VpOkvBK2;>Q0fROUX&JJ~t'
            '@Y=V}Lh4kaTuWi-65Aq?p$}bY*e&=*RXIIb)Y4+?SYikH$ZqqhSk~E6-lj!Ub#+5;Vp-XjpY;pO|638;E0{c&c-'
            'UBnpRZJ*m(qQmSIsFJeCZy*#gKwUt@+#9x=If%WAXPP$l<Qo85Xd~D;ek}Fq~+W>Jaa+@O1IgG9grqSd?zJL^B$E'
            'r(bde!G39Mkkz45-#$<}TMgBnBel^fP*QORLcN-}hg0rvvwhuIQM*G1DyxuzLY>ctfk2Z;pXi-'
            '6CKwY`A37Eu@qq*ZINOis$jwdZ&6CkHaBf%4)gaxmVv$2PbGg1{2JCIkOvrgIimrWFO09G4*&pMqIpl0MfxfC054'
            'w^t_Al|SHWX9iZZt}eKK?KkKXBGX=Z+rRexco?Y02bsM@S$PdC$@`xnCwVd{o#!Ouh;A)zzSva3Is(aIv0LHoMc;'
            ';zkbO_Qe*m*L3Gl9ok!h^-Y15&jB4mxS-z<C4QSW`EW28IQ;n6K7RCSb{nD5vofK14kgRmG|q}^-'
            'EZO0HwM+kWRX0Ly9_<dyp~(5Wt5Qk)g$Zs)SIBV;987Q-'
            '@sX~S52IUM7{m_%KqupU!FZ`Y@aqsgAtR7;Q%Y@HD+rxxe$16?*OCGA89^~thT5L5#Ya00O1)NKhzMcql5g`b8)G'
            '&Dzq2!OIhQ^Ex5L3yOQPkW)YXb8OVy~>V(Q1Z_<T`OR^|UD%DSeh~8kOO={akhP*EPP+phISdhBAIpn9IX5cyfG&'
            'p-'
            ')LwG~A9+bs6mZhO<4yYN%VMN(SDo2T&zV^^eTTJxTJ%$3}|5dAF0F@9hOYCF`*x>k$p2NUiOe4*J1gP^0$0vY=dd'
            'Pw%D9oshb33PE&6q(@h|~y$0BP%8aX484Zn~npCsX}8s3fTcM(*Ij)AC6>c(d)gwKpT7ulIWKaHB;ZJiM0D0BG%_'
            'wjGPwca(y*13|)5V=T(e`m-'
            'yJJSVN3_4fjEXbvx%fCAIw(F1V}0#wi^0E?}reAH^G>`JtyU||*EAU=A2XX4!8JYV2^&?XSV!`xmno1%)_0_KMLc'
            '}D4}_JyQ)WkOrM-+?M2zITw}b3;xIX7L2aCX26i@(H-'
            '4Il4Bj*d`wFd_&97jT_RY&S61gAMx3)8vF3V+3E2Iz4sCpj}I^W@b;Mtk3TGC&xYBz)abh*FLu`G<f=tw+aeC7SZ'
            ';b{;OjgKlMICBymF7mPDaZvC~;KcWaX8;<8(YNM-zKy`hn*ETHsJmkcDG`+!+gI=a?#8=9f)=K<}VP%&#ddQhkq_'
            ')9HDwnlwwIvdJSVFXY|O(=68NfokaMs7S$Zg0XHqu+7<?$7n8^WFB_mH~5^VpOj7Upb{?um3-'
            'EW(s<xc#kd!#iWqJ<D$nG!)H|l$=Q0k=K6#$nWG;s&axy-8YVc|~;`W@SW(cc|niQiE$%K-'
            '(z;8?k{xGF=FnW{{FIMi-EEC)KizGKgWwKJhM6OeGs$m-'
            '}rr}AF@(ip$u;z`bZL#07+sU|m4fTi)C?$B^whqU+GqBm@8AkS4Y?=&l!LeOEcblNTcKYlY<=LKI{Z<xp8-'
            '=>DenM**%dA@gU#l-XCdz!{>miMavV*F_#Z&G-3%YpL(IgQ%xvYqNW}26D(U}tNVL~PU=cqQ)crN7)-'
            'ZNguWkRwmHs7Xy3Lvce_`B)W<78cnKIFwGEjRwy!VIrq3|c##l3N5}f7|VKLCk#eaoQ3$x=yjXX;IK<ISrPp>k04'
            'JZG1m$A1z*Zo^~u=joN@cWq|6seeBW>F>}zFKzvB+<Dz`ynDfyC^=1$Fv{9Fu9<a1Svu3_o6!02K2L;+U;SR*0{T'
            's)(QSsa)w6&(k{XY%V=hYvso_hOZ>+Ru|khT||z3<G9hfi2pamQT^<z{=wx!ZHxZE$CWx{RVv2|$B*5Pc1$Qo2no'
            'dMaanEtX*UZ?dLBy+?Cwx$9D{B_e}gG3;$=;Na$bUeLh?xzwJ#Ck%R~=X)pSdmv&%oeO@xwcr6w(<>_Ox{kxI?8`'
            '0YJ3}Q}+wMWdoII!1atgS`*YZ!ry-vfcJBgz^&YO@rIM|jx)LmKXZ&iql)~71}?$FRtX7`vSc#H&m@t>Ny26lY{r'
            '~0?27MvB&f}@vtj#txp^bHIYw=t<SNj;hqSh{LyRLm83#l(#Fe-'
            '6WNjCrTBxt?6~ACp;{{vVDCQ+e!kB~Yy^)zx7!qK(&fuEI3&RIb3cF{X4o*ef}Zc6ySC_%Peive|&cQd^CVTO1o7'
            ';*)PKy{G)6h1MgCC9@j8g2?!5D6kQ{GD@7v`lc+JYp<eKz0Aejib3(yrD@oyNUg>6#mWQ7+f5h=791T~vm=LMWJ_'
            '3{P!Jm6$~Bvhv)9%B|7KtdmLQuFx<>CiDLs<Ug8yGLFMU6O2uvxuE5Qx_FU*g=w~EYHNkjPSc49txqU$yF9SZQBZ'
            'WfWL`a`Yo3|sHJc&%y$dWccVESM_D3wkqjrggYDK<z&Gb*0W*p8TTHiDG#99@mg%aDV5hgT-'
            '6*$<{lW?T+<gHwrNUAr3feo>-iN7cVrogR%bn>!|lLuCcg*BaVXB$Dvps1mAJoUgAldiW~)WJsQ<u-'
            'hqbCaUD5?16GvcxFxfy<DC<Yq(MLOFFB@zM;Z;*1$v0+urk>0121p)G=uqdUX)l`5Unp&YrM24O+<j*TRV|Oa7KR'
            'E*Ncr_B5<5XQ6q(Qx~_($8jP|x%&qRH{ciC{1nL_pY~i!61$2SN8^Z%%RH=)1QmurOG@>hTre?eX7_WCU%+3sqzO'
            '?JUcQ5<BOMVgPc#{=z!srtQul0y1f3gQmj`M4oc<Q9O%xW&mPC!lCBT<h*dk2qefhm81oC`}!jk7Zk+S=5eK%MA;'
            'xhIx7upJqgIU)2Y!%=7d)cug|!N|Gi9JdazAHkV34}B+RTk%*mJkt+a%`*y&(^P#<b)>)6QHa30r)L3q*s9kKEEI'
            'KbtEvWS&D-jNeunrd!I!iS?dRRR*!d*e@AM-D?aOQi6}#bT?0n1W-'
            '|RhomtjNJsJG`!$A9y7bku1I!#=zUf8uJ>IeFBRfjEgp|97`f<tER~N(N4~h4X3st?~ZMu+6D)YjU~!w435RLBhD'
            '>Nfb{0)wvP+UUE@_Py4Fg&h-~v_M6-'
            'D*ErCk3UO2ER|2X(Y3~x+Gb3v3;BbCwK09eCtD8MdJDlzE`Zw@SYyEZ`m#7zk%uyW^4nMxivByu+idQi238DkQNe'
            'K?N>fLbjRN`mC%qH-'
            'A(%4LN@P2gTN*^j4YAz)1r>nX>Wf~4{t<=5ia=$;I98dPPks+jb4DoKj0`q^u;MK~i^`r3mM)#+q_UfR~-'
            '_xgYyB2BA2`RdBp2H1Vqb^J45`Ipg&m0Uuf)NenL=k-p7DY%*6sga_C_Ie@{|!{j9vJ'
        ),
    ),
    'export_mdif': (
        'export_analysis_mdif.py',
        'e135b614766ad58323aba987eb9b6afb906766dd357fe795066cf0ff8e99b627',
        (
            'c-rlK{d3z!vf%IhD-i5ng@`HG&a2ycPhKX+*p#g*OO_=$c{y1NLnJ6+MFI=}T9&o?-'
            '>*OB8v~NEop*P2m#SD2FzD&&>FMt2?&%4`aQtamR!wlccT|-@eUmMl;ACf+R_P*ZvMQ*udNptApecjPtjMZ-'
            '5*)nP--~;_<5dwfS9u-G@_82IMV(JGc#s9<GAjhUWmWz&n>0Z>Ls<B-&gSqSn+9o-&Tnh@{3@+`qL(-b-'
            'V|Bz;lt?pi_z)m!-'
            'wEvUQVt9XmwNNO#^V304M#J=JWIddad)tYMwTESv<bXO2D|f?M>1;8w59bb0v{bgMok3Y1*Vgwm@irL`|cC9)BGj'
            'Lw6t3`6{bnaHoLk+a|au%cgFsbcrbB1t5TZrSthM4rI17DT^k}i);#*Q)l1T!Q0VtInO7A6?_I`Th-7NB2=!LU~-'
            'ifmw9m+WW~q4DvJfc49Y5)=NDC4-2%4F6%t|;G}!{C2A&OY7MilkroAPMc2-'
            'u4o#lK5P~gQhuaLrkA9Yg}fLlHb(x7hAVw%oNAm}_@6_YC<KzUQtK~V<javAr+FzoeaRk;X~WVUKnRhA?{z94o;i'
            '=u332z9R~pH-JY$~u#O=Rne?Ea$a+@Xxv|<nId@hWx!$Eh_bKy}AJAm}IqjSKq2%apcHVjNPQ1BhMf%ae6V4C?3E'
            'dfR2OUB>Q8P6%)}K=XWws>pH7tOZA9bAccY2^6e2~N-vsQ1Sp@6irZeV_m^Ni%^PIhIt!-'
            'RETz?Ob0t|ECL9;S$)w6*<xI-O0;nELh<?yhT_f36ILW|PFUEVLcdt*AH}6i5-'
            'kl~#qtjQxFo0>0FGh!>*T0|apCpH)gR%YUXmkwEPRGae?u1?j!C!*s*yT>0A(sP7KLg%gHn%}W%Nly0&lTHi1dhj'
            'h<Kyw+^Kr6&a5R1~!r$J!IzXuZ{Ym^pwc9%$zkLVoeoqeGydZ?q`kK1Mbz07LVFg_ef&w_@BP_aQ32USt0PAJT*a'
            'PI~&HmvjcJlPe6JIAMr{g2+<Z1Bo)#ngsf08x9X|>8w{M0~HzX*XjsL~rl80=hD<!Tx5(kQDus{s~Bs3uEch0I{B'
            '!TP5)$ifexj|8kYt7f@s;>)ZVNhx!p;O<ZBeiQ?&Q<Qs%PhL#sE0BAz*yh>evRcCG2F!#!14@*PaynDo11}dKGwN'
            'V3o!6Nr(=WdtjZRKrYEF2DUhbcq9*<7<-y8x-'
            'sBQ0H^q*d8CO}U7zt>Bi?;k&Zw|}a^yao`zj)~W>ZNC@5f5`LwFk4LPWLg(t6g&>XX;$Z#MW}y`>%0sHM*Ewxy5_'
            'bh*Tw4y7RmomE36L-'
            '>2p>Lanhn5JpwrjE2PO6*)G9KwRqg6MTQTTx2Qf6T=cuVBIzj!Ipb;Yuiy{_nhPhnN$X@%Ww-'
            '!#QE1Ppg&|?7g_NSA$tJu}GyH=3hw;|zmE-^d)B@uuwM)GlG^^!2JL7-'
            'hJuZamd=SKOd`@j=6^klh$mHs?Y(JZqX=Ahkrpx9E8o^QTSV7r6fzW{;pSYE1yJ>8D0+ZX9RX#n&-'
            '|L2l30gt?4SY<>QDO}`FNL0P-'
            'K3MM1SnZLxe~k%YmlWtP%qOWCf$PI7UeWEh=l?onUuf}yQojad;(vpX+_yV#38ac4YnTEadwIPB}atPDl2d?PxWv'
            '>ho-1Ov1Pytz?3d*JV+U%M+8f~YBYx8S!p1>5zS*F*>N_@DpXt+nurh3ph8_<kz5m|nPNXdag8Y$1VWM-So*ouc#'
            'LXLzmPhDmZV%}y&lM{AOYCaQSwKVNCPC{wb_q?ou3d0j{yu1P~)*|6cep#G=2IZFwW{z7;!`VugbvYC<1tK@yDmh'
            'MO>Gm4@fWsjc}6}|Mp|p{`L=eF)eTEcsieVe?3hrXczjso|Ka^ji<NpJ42|_9CW>qS>viItNtu}SJbN|k{IX>hM@'
            '$%8{C<_-G`AR8VC*$M?R9ZWF65Ee^HDus;{vZoLFh-p(Q#%4lQ8f(+U<Ia%(!FH8*;3@_2lJY(nic8xUI`-'
            'JU>)e~aHX&q4f2`{phFVc4pJ;O%R+LHCPU*)s)j0TK?D;Ce=&4-A#N3u?A*&Tw4k@bTF>gGAz_(`h1G-'
            'u9Uh6(NxG^h|+8um9kwtIPREn1vx3axvfp78lsQ6{u$MQXoS*;L`-'
            'RG;dC5B3)3(1?mxSjslL>8&KUGj`gYWA_hg271O@_HnPVlNQm>Yexz-pL?&u9Sel6MfTJb#>(Iul4TRLSYAukX`9'
            'r*F5(7X>bM9k&*0-LB-x2lrh`&5i7y@<<Kzmds3CNOgT1O0KrguS%6-'
            '<E3r14xM0=C$$Ng?ywHdR_kn9U<W7qK+45%QN_s6Y}B)hz5C8XKPwscBrHOZJT)zHP!y-;<m-'
            'Y#QPQAW}bkdz!pG8YM?y?CrfdK7e1|z1%+}qc0o;_}YA8kc~mYB11T39SiVi|MuOk08kjkHOxiRho-bq&6bf(YM2'
            'LtXFu(n1Zpd(kH{$cbS^)`D1<rE?H`-c%33-'
            '4gE+70XFu{u0<)#S2)0ib>ExO)u2G5^vo>I}nB;$z&GJtX+i2ORY_e*|KQYuz^ix+%;jmLM1JF3dQR|k1>uQV5Wm'
            '6Ic@w~i2$wz9AHsg*!uty+em4d+?MAj!4U`SunldEM0n9h)CVJHrJgs+aq<C8ag$&3BtPzeI#6NAgVNDyg^_CgH6'
            '{<SKTtCCcX+b1Zw<2SF~9E^33y8Tui>gJN|Se=4aqsDEuCFh7%D$I`!d<#`2<q7`y8hwS{CNQEb=0-'
            '(j^@A)9!~~WoD+hzTaL2kHyxrK<bM!Ro9zBw5kv0>O<2H)b<-'
            'EM;8_P9niwhVVeciQWoux}{A4Wxb3geqxlQn@mEvYe0)Yu9W`pA$-'
            '=jQh?tql@q7Q*{gRfACmrXddYKD3y}rl~NR!1m7PC|<(%1=xS_KVh5H7my>Qgv1i|g;@~xixM}2`BYkh46D<6)yp'
            'C@Ojl`H-'
            'Wh}auDTCkr%YTmgI(G*NLNh>v<3A$pWnvsi_icj>`EA@p(*d*7bjwjyEvLVF}i#6+Yo(bHTlfy$J0E$EXo>f<#>6'
            '^o?EnSvrk~%iro+TUMrBY@Ndjul%Y+OKvSDG7|O_YT?dZEC6>-ZcPqUXtBcLp(C}!+)vD-QJa-'
            'n(r_+%90VZbA`M_pPoaQ0<dYl*OlKitJd8cSEX*Xzq|D4A{np!IX9p0I}B)q$w=jCcHjo=z>e%|v~{6dorb5HPK<'
            'HLIm`ip?C3d2-CQ~d#9GoUm~y&?73^efn!VTwYVDf-'
            'JF1^RCQE({QCT=y*lIaEv=A{cBzug~RtYlQUZ{Yy``jMmY~7I)!Wxn?X14T6gmis(O9IqvD%>ICr-faVPrd0pqlr'
            'M*x>V+xta*|n9FRYJjp<PXF5#XE4v$3{+^72=DlXQ#X=XxlnKoxs4v>Qk?H*`@HfT#^HmC7s?$T1+op=PUqBMjO)'
            ')^ipiaY8DBlKmidg+3!MbS24t*B2J9E5XN&d6<JJ#&XmA#X<RuNZx=8%=>IvoZLTmfqb16Ky1KKiG!TWcF%u?t`*'
            'zm9<x?<FRLH>$0`*)Er!))Y*9kpM64xFuW*K*A<~9hO*=WS|l^K*;Q70Oay}uNSQgKQ@HTV7odIS1!z&__ez>ce4'
            '+w|Vf#lZ+}meSF~9Z1pvmS|^B%V2bNMj>xvgw?DdU8QI=fn-T<0S0=9`!1jt`zHY8_mJ!=_vLS+-'
            '(QaoUnHtg<l1Ov4;Ue8<1SndcVRi30fT2*fygfMB44EQ@ZK>kH!LMuPKRY65JH?C9Fa+MAQc7hWtA?kP|@>Zik;O'
            '&AYW4?k(oa=zNkU%0UtfH*JqhYQ=*z+xJZnPoWijUU2xb(kd0#Jw02WVjnSuHXQ+GCXVxy3dA7<v=H;qx^M?G0=S'
            'sgklP}QzcQm%OVX{PG_hRjzor{fLPN8FKHz&qm&u#}UYACp=Rln=CF3dwsSp2&Sa=a{;iUhpm#T>{miHa6EA6m4-'
            'ji-'
            's1oD)JtO^e`dXKJF}1Lcx25iFN<WL&CB>8~eqw(g4r1oCQ=qNL3ohGllm&dK)I*1mMCh_7P?n$<A_jm|}9Frm{#_'
            'GtArAQ<Fcr*7d9cSsO`vVJ@x(>A3yYqe*1s$IZ#!i7jo;9$SRUhkO+IZH(0h{Y^9{p!Ad#o$wiu$hH2f*Rb(orGH'
            'd*(acS9H@w@LJ7>r?+3y6Y;{q;(Y-4dTpx`yCuglmf=S6f@oXyFZ=Ol`$god$H$r`K-t!I|hN)9mm``eL-BDfu?p'
            '@?OfY=WfV7=x`W7M&Z5=^d2-'
            '1&6yP$dI#$=7j{4TrK#G(G<AqlcHXU4){oETR1Zwk$95bY5Oce+#R=0kAF_izI2xW+-'
            '9yn{1)Ej0_UJd$e+v6yIU6GBjGr7rVwo8ngcMiT>5tby=%W;<$bxDkOMts045yJwY374pygJd+W)IQb<xKa(RUJe'
            '&nw1!}6Zxm#`z8>M-8G<^s(vI<kbG1m{b4;*UJwqb{e_Hq*Zc!rGjDkp&@RN)>DdR~P*%Jp0FJ=YOU<pP%gfM-'
            'uOxKSJXt37tVjV&@2NB8Qg}WFp-e^3X~8F~cW^@a1;Aq*iv?Vy9VnXQ2*@==*AhzC@LVavv|I`OIWNj-'
            'LYxb<qET-Uj$%7Cn15n$OjnDD*I%9NK!uqaH*W%Q}u@KeXhn&Iu)sqb#pPB{n2T^Ww6PJ_gNI(|pqCBnP$aJi>2P'
            'YLv8iRpMQ}0_zdb{P5wo-KW7~F$iAo{s=!me9${h>VCTG^Z?U)cdvZ0(57L(q6kP-;rsfBv%#}-'
            '_yJslxJoaB9VOzttg6}Q`=o@b5*^>+FeC@VkQ@utHCtM{{CwAa9=aVWXd8OvFbgGlP<*p$#PAe=LGU!PnnODZ1h_'
            '60350&O-'
            'b$5^TM=quBgRv3hE2{T43nGqy%JDm2KK$dFbhu2>sRTGw!C}{gSsibK^5xVtBMJSR(Y*<yzl{mXlD|1@GX20b-'
            '@uygtVyxU7a={f$2q<g956}-KNLA&q%gxA!SU`YUva8qPE2(3{5%T$j#|ZO#SvFpFdn1scPCx^WXa9-'
            't~nm$Bcgv_w60cGR-SAF3@DwL=@oqr?*R%K?B1)in^wdeR%8FG>)7X67*}WS!33)(IDtk=F@;si<lf}(cnum@P2F'
            'sVxV_2^05gRcahxN(ce$cqs{9QJ^-'
            'CU9KuM1_%xJTCwJXBZRv5Vv0R4cCeAyzo#SCMR}9ABG(moDDHf`g{3Em0`c~%8I?;ZN*^|rF1#Hd&ofCNgpT9uS4'
            'sfo@X)PUzLiF$OB2+;$BQuPb-'
            'g=&3phlz{$a*AkC%&uEP*^&T3_fHC#)Qc64ou*_i2>4M)B`sxeQp|U5Z@HZmFd2OZ$AQN4GF7JG2MfmFNTTU6?qd'
            '5A_tr|Y7Y8*N{%yhxOECzMz8;a>O8U;dc6$rjz!vwvj6rcqVssQ#P@yGvMsxGL|Hr8kYC$VqG$4i_=f#;D4jzi3B'
            'nPZ9dcjv6-'
            'kk5@Pxp;&KhCU^$n2L0uoK7s;h6ZY?*KtW}p7(bS=Q(@XUc`JZcW(@v^XHKO(wdJBH!pYd9R%#a+O7TX7f<Mg~Bc'
            '0@RP9FJobH*ZDW%E|JdK>j>)d>z;+BOU>naQi|`qqSP0#=U84RDHz<jt6Y^b?1FdhWSOBd^yy(CueS)yRVa<c=nz'
            'GsM{q|!VnvigcExCqgSEAj3kHwO06W7p1FP2#N893AtAjCZAvgyZT`rg$fM;1m8n9w<c|1c$Y07GfVO*&QsP|oOX'
            'LbTcZ9tO9>Y>Vh40d8qmR^|lOc3!Bd@0+ghE7XOU+S6rvFDGvk|`3k<WGAd9HDIVFF*9imv$(@<Dc_tqDi^9$O{n'
            '>D)e!k7&fib)uieFU|`^?Hk=cQ6;4Y3GwdJOdtw5PB1>A*XHr%!%Q{C^NN{tS6syHWCKi?Eu)GlKz*>vk7Ulq6n?'
            '}ug+p{y`Xt?j}L|)-DrNd0<Gz{*jGhQ%mJR7Occ>R4CJXza^4L1j#3>K@JqM4E?yTKhpyLUF~{8Z^1y-'
            '4X;K))()D03cXVZK@v^hYZR8(IZ_51u|DW0D)v-'
            ')%o%cyb4g@9(&gaK7r7XY_U;U!RB4lw72sWIrWMna~kEcCU!1?7i$rLm#wGO^7|1abluJ19Hw^fV_BK79TS_i6+g'
            '^4<FF<Jjt2^>iEM4q(+I6DdVgnA0pK921bO6q$VEduVGV1_KVTQ_&rY<Q{}6G0f;&>rme>GUIBLvk2!H}ZH|KmFi'
            'C#D8=UNLS5gPof2=U|zzvlnXVpWT?)qLb7yK=LxsPHiErG2lVgXFy)al;Fp%q|)^HvJo4efKGlU+wv5s$*V*4PDY'
            '5I>1mBtsRF;o1ho#(>2Zgmal6DJU{F;&yD*7Vb82q$KTo7qlAIKo024czPaLZb66Y>%`EuTtO!WW0@O1gWY$NpgG'
            'R5Rl7sjJHvKa*z#ZuV$@eT39L_J{l2e<fZKHaB0_F|`fd1J9!>~w6RpoIsm=y1mKWJN4oX(qhkI%XM+(iYfvT}t?'
            'KbI%^^>E|ER);RoFwxg*=?c_r(9?`2pPUI4xGVzTAO`3qSW_5h~Y7*!H8uQt3+~36_;7x7@f?V<&$a(GX2T9T=*O'
            'M<nzMeA4_m1<t&jW+6?Jo9cXhTh=45FvjyKi5r8u*CJ8ysJbw1z_~yC^yCbyjDcpBw_Ij_*#D*S_ie>K%%<ki^2&'
            'e#>v=?6Yl50~U>0W-'
            '{k`zMQz+&7{9j5b*WAkyWy=;kn+hYNie*gpb+86+pd`JL=j6eSzTCMP~I=akebRw`Z#Mfn&Pdka$T1HaO*t>orqF'
            '7XlRUWd~9mS98Tld+XCfOk(cSeBE{YqW~u~R`eO`P@wDMAepD~S<&iQ5%p-'
            'UbfR?U)c2EQs@ZmKU&5(&91twll6LR;&;14_HCH>0bYI_~X{@vW+?ie5x#+li#eXLB2>YqgKMc4n-(x>e>Icq-ZH'
            'Qm9uh~9tOk(gz&9DQ%vkp)Fwf9Z*?@Jy}0=#8W<4{xeFOG&-'
            'Rr|ePB4$qYkH|_*VKC4Z!w6@1e<vIuV+b=a7F4Y_CK;wApo_Qr?a8|G$o2zZ-'
            'K19T#^lmtYnC<9+=@|LoDu`Op2Ici&GR;lJ_w=?~G*|H7Y-'
            'B6x6?jnAnG{{3@=VN>yS|JCPzUBmwe@c&Er|Mb=8=x2EUR}rO#{`OxUzBwL0ADxV`0DxI0;@#`h{iE0W<6|r~z@f'
            '45>T|doJdH)NMR+a$&i+k2S*Ry}6HhMHlm8G;8ujGqkAvR56{^<844xjBJ_eY;;9u$(x!fkx-'
            '%hwXEo2DYIO`6Oo`Fza0SnHvy4EonojFVeWL|wXV;XqgWf-`#6wg-kIlb%~Y}GT*xp;!0YZq9!XQ8Sb45{=|luK2'
            'sW>(HI<8>Nb+yc6T;2Qt2S5<g`&tBp`!0V?tC`U(vyZ};Qv5TQl!hAl5YHjqNis2x+Fmcd)_ai&-'
            'Uwsav7(GOQ&QwG=#c6-'
            'qW=QZq1b&7(L)hoNPMIxWQD+kF23Jit5#>f+2xt*Tw_P=&6Tylq!&!49D(^((O!dXjU2p9LV$JTN445!WE1jOjlt'
            '1fG68VT)4KXl@sJG9%`#R{$)@?9sx`w;9@0w9C_d0@erMCGIsqSkBk9`$P9;#N1Nh9b1Lzi=Rku^7%Wc(vJzkFu*'
            'ofnHix8hw(K0&2{xw{y8hTo<y@{gaol6@V@+WhV`-'
            'lU$xQH!Z<X=i3KN>1;<%U)LBa%pWOHxX?h*WS=2LT?MVudV=s3sjUSxic4+6*6(w^EBi1cFgSFyrz{`Ry5^onr#G'
            'yo4pxtT;Ae^3_BTCN7xCgwZ;W3*Yk4c;b>SgDDUy~0v1GDrV}781Ee}_I@ZL7ysL7IJi`E;YV%BfU1eNWEpnAm3p'
            ')cdSve+t`nSt_&~va{K7rx4VE)^H(Dulvyi7fPSV$(psAPVzf_cT{vpzoarh+Supp*(44y=g^y5f@<c6k~FRTYrq'
            'B}#?Lx{hbLIVcE;(TIBM1GbWrLR-'
            '&ClSSo`wStM77+g@t7fxjFj#HzDy*zf32@384xC$1^XI;2wZ+u`#EF4oU4x$vEGCedW=p0E}86Xlfuz_aTLg8}+U'
            '%ZA7+z_&r2;zc`9&o(v)LZ}1$dU)i2n^sssUNk>F*{X@h#{OoE{f6>^bJnvwF1!ol8(+S=|iGx&eI9D5spBINgO9'
            '2`3D9BoC+p@#hYREI~uxYZ%+rh?8OiYt_sBgH%EKYdIYtxXN@GdW6#8+;3+zs83LczeHP@GMd@hH_HlEvc`3%*+%'
            '74nXR{OmWa$%(dK$pz*<}h}JqS)?gTQSgHF*dO@sWc~UME6o4%<$OkY9x=gTggly)KBpCe*+jZRE`&ah+7&1P@ue'
            'OKo9rOnk^t&2-'
            'e6Iq6w2+d4wVZt<}eKauYk9^u*JbjsCD5ihR=tH5}cR%>~6r@N##iCwu&ms_*QQ!YK!u^<>m5q=Cx*?>(7Iea)-'
            '6$G<B+{UgA0`>)QqR?d-iXTdr{qpeP7fx%r^vvpZGwT<g_}^bt*8PbvUl0|l2TT5Co6F;1zo`RjYQbK*HK4KC!-'
            'Zt$!b+F=wrsGPEO$_``GSRnuu>}OZnE{EkpT@4a@&3r)Y?<{f}9l6|3YS2tVN}of3<Qc9azd5O1C!{MW4p3YfKc7'
            '-<w&|>m9$cpAO%t02uvw5&$|acErvoE2d<FuJZ^h!u&mW5<g+z2M?Ma{F#V?NT&V9c4$hZRQ<$112gQV24<UMqCr'
            '!y5uyD%g^1cP{1n_-G7FwXe(y8MvDqx6vzLwtYHgib9ks-'
            'f)=R^{Wo3Dgw+$(dTj++Kz!uvw4pQ3~HhjX?jhZW4WO!#-'
            'GI$)Szbe#;^5}cmL$^O}=sVMN+44if>cFHF!*1CU07!{pn|?kmav!waqq9)W_VCU-'
            '@$Iw$!>W~WImfJ3(q<rMT}IYbWhXX@zjlvtMKyia?WEf2J!%6s-'
            'O45xbyP7ahjXC>?t|buyB*Hc#l<wGBObc}or#F`*u|fM04?iXBNFI-z8f0P&vu@kJL#C}oi1C2-'
            '&tM+j``@OZHJE-gX8lN8x@&w+9Hg-'
            '%{RWSyGYiWXL8lxv)B|3>Jcw`yCS90jT|#MM=U5>P(*901o&Y2{HR{wxT<VC{bJ9W3e5B8Q{ZOb%GE;tu?yIiXy+'
            '5J9bvcf`cZ$lWrlS!Gc`Du6H}B6%wwfPex{>(CwR)yiDg;@ERo?Eb;zmx=r%Nq8nK#r#2@@1;@6MO9v&3mK3BaUX'
            'A2BWa^WkNHWd0=LlnEPvY#Yf1O8)GHhD(rPt@eGihXn%Qt}frq}2C6ZHNGDh<TxOQ)kd!_w^0ACUAF=O;y$P=9a6'
            'yW7&6Cq<6&uq~i}OR={S+^%}MWeUYVDh9W@&_mc9KE6gm@BoOYGbkZcM7{IXg*-'
            'yjZDVxts$jQ8{jjRd@%{a_%0~i=uXPz|We2CG~9SoN$v-'
            'qNJzYy6JtNENDRbc7Y9`vx(qCEt%N(fotA($(Bymr<cxl^nzBD6N(|NfIM&`-'
            'UYbzjFqvu$`tl*qbseBFXATsG=plV@!n#Nrs6V^5JKW29(dnel^)Y<lEK2aR<V44cTBWIjn_YXwR}Ql}frWz-'
            '>!E>`(`>I63WqErQ0Ol}E$r9@c_4a``HKddqk8HCF9yjdaJRpdo_d8_!o@<IQCgP`(8Ip5oocV9eV%zDeBlCEeGm'
            'a!8seM#Y78aXv#=<vXri1x<ZQISQ|kr(8}C|cLyA&<_;xLu#jqw;tD^mrIQw+w0z+ia_Qp6i+RIJyNis_Li8!LX4'
            'hZ%t^M*k)p(sf@eK#C6!SoRE$?$1;m7k4n2$xwIO|9jV-ox<}RUtHcse#)-'
            'K3R$)fNNz;*1;62uE_uXw5vh6bnI^*zu!`H#c2*W=F8*PcXXs9T)u{kfPz$UJHE5lr~1`2U}Wb|fNhHruR>6_$Pu'
            '&Oi!97ma?nZ<WPHGo<Q%lNK^1!_!B1v%z~XI`Jo7b;A9%WY6jR^@F`&e{Nq{c4>x7S&Y&o=IL!RypWR-'
            ';pQ#<=3Blva|b5Iq27hu4?->x^dmnD=b>GgGc$*0lE(#o--AkQ&@%f_!XUuGR;DpgfXYDy_p^1{Z+=v5#zhRf8F5'
            '<aq>ktMd+R^efmY8i%=(E90Uy}5#g)0-'
            'rhplw|a{4rzf~;gYCAk^ifn78@pDppS@5?ug?z~xN%K~$%gGm9o2~STy1w|b8Qa2ul}&_bc*W0dj<;)WqIO?jAm='
            'YF3+ur?RwQxC3bqdzg^@>p5OZ1i;*~9_zxuf-;>9l;n?x6F0rE8OYDSy8t7~G&}shO^C9w_gWHL9(5@YI-'
            'Z;bC&hr0H+4rUF8?)y*uA(vje<Qh{@o`S14D9SO%#eVMe2vGONS;%(zN(tjwjJ7eW<s~`_N-b%s;Eh8!z7+_-'
            '7i)|X?00DkZO!MSsRq&&80&`bQmako!uIQl$BNl6%h$&U;x710e5oVbFXut)28zDns~zXJJ~;E-'
            'ciPTbF;3IU1Z2ZF0BPbod{(k;rrgYqGh6pob`FD@)b{qMN_M~tgt&5@*Y!+lRz(uIMKaT;;_3=lB^={D|BI%v+cr'
            'I<_m6MIx~gPOucCzT`;hcYux^{z4emA^c0=LoM|z{HGYVr_BFryy!LJof>zg22JzUgULjGCJf$N;R0fl?pqv60D$'
            'Ii~%`#k~W|38SPxK=$Pl^#fQoL_Ip!%K&ETYvyU}aT7ftS7_FyT~R_#v(mtoy27Cf5sfin%y952`B2^7CDPGp7!V'
            'DRKF(1+WvHj@MnGinKX9H!Hboi2Su#(^kXNU>vFM10*gsb5w)?rk~KYqDFlwn;zcimqVSl7TsP+b>Ka8{%(IDd3@'
            'L&o2sVOp@W?QadN1dyNIRK#aao<sRV?Rdwm@ntyGJIukv){q$rxFF0M1R5STX8Y=V{T`|X;6{U-!b>S`@H<ol-sS'
            '0Bk%at!HBB27wXJh`z(oW((RKB*n=US3Sa6%*#=o0BWpe*wj$?SqNfybT^7NHbR6|Eo8>bPy^rWQ5E{m8f8nr|RS'
            '-wnl8M@@JMP5lTqIZBg;;+~`>>2C4$9zp?AUw&5<>2<7{vd>t6I9h0?JKejftii{#@+3XNR8}<0*H`sJ0Ez9d{T6'
            'e1QjnQ`+jr&bm%W6Y_BO&js7*cCXMlU>c?7GvdwPWaWACEDx$D4aD%dD=(YHw%EhKStyi=jI=46Uh^0+BGXwWmz`'
            'a6e(ordzI9tG2Ds_$m~0#ST=$IBP+}a&r}z@Mo>neM*^L+{$&LYr6W40EJ%c2<m88OH|u~AfL)~5AM@W_~-'
            '!I(*<20sHt6=6DMpb93!(5tQfcuUM^TW-$|J!a>PRqk?9r*KXKJ>(VwM}UHnNsZC1((u{G+r-'
            '*HJ@n=DFCd%q9~KrLE!g(9p>LGRn>%j|(kIj5bKGRMfBE0!f+rno4lt9fQDP0wmwzu6Kl^Xq(>kZ`T}iuV5l+~HK'
            'd^mdunwH8e{EtR;y9?^uxFUET#6sy1del$8c(L(m+{>kYv2--J?rX*5+4Q*}wmd>wbRWqj+J)3nkrG^0WRd_32_A'
            '#q4ubUFerAOPj_L(L}*5Sv>f7f}_v*t$|+vY^Z!j6=88oZ%DwOr_NM)wiWBdb1UeBT9QK04a}zLw_?smvoDITtln'
            'G38wO4B#UH$2@mOH5U0hx=I6VJ99r*E-'
            '<I}GArQ;4Bzn5^tx6VdM6&VVUj0EZ(JB&<)qCwZ|9LCv{4k=kYSy7vzN$k_d&L^M3qv|8=-'
            'Plk?3`z*jR2|2>%^1PloVsB_?;{*3M53jjQXm=&ZeIvA)`-'
            '`T`ksnor&&BSJNIJgR#YtudB1m7YXTa(97K1y*BsB8~!zlqEY;TGVkAWXg+=S%KPOH!v^3Y_Tu(HKZy~E_#ubmpn'
            '5GCUy+`ou8N7kJrwm0Aw+nDs84r{WX$pUHW*)`gX_SRfdHMYJ52Q<@NZ*GZ7@l9TFmISliA)V9Qv{i^+U7#gD)a7'
            'Kcyp%C%~Fl@^*(;;uzJh?2E4D-6nOFQs=%(4WXOw->E_R|<0%pG$2#(ASgexx*tn2u_qOP{%*H3W&-v5>rZz+-'
            'P|yUMj(Olh5aP#6}<AcL~B;d)L)J+FaC&h2*d4OjIh7kC)n-JmSmgt!IuEVjS7D%wT<P(;)t?-'
            '_=h>q{lwar_N2R3GS%aR5kA5Xq|l%E=^lt&@79JRq>=;-'
            'm=Hq!%Q^5yZc_tWOI$X?jruC+1QfPExT6%^jr<$Rt;}|6m{E*TiBz~rqb{0FBWj3ZHmK(KCiuUH9P!>BA_3&j()n'
            'Wyq@T_m+CzH*q^*xv2BMK3o;b~Dh}S&Y$82B`BmO!T6G-'
            '%BghvStQVM<RYATb^tUdvNj|#`c69h{hu2v;Yh+o2YJsiSz-_KnWeA0)ir+O?c=X&bsQiH1oZwD?5EAO9p_ZA@ru'
            '>&Ngpot#cl@s3PP=?zH`(GusNt>?7P_=j1d$Pra~512(Zqw6Sin5+7$oG5Zc1^FCVEgwSE#M(zyVl;g|E`(QuO=q'
            'jf>_*fOr>D5MVMF-(HEi@Y4R)khF814SsRwIhpEeOaf|il>(HTf?pzrvCnU$MX`)<z&Ma|+Yt}fj}rN2$p-'
            'u7$9DDo!oWzFyqXHoJ92<DcG^YVIhcLtJ(259v#O1tKE_;O%R4M?|B{y&!wiY@yAG^^6V-'
            'LS2yHA;wkf3rXL#>;TIKUwwOv3qa6pMcUSQ-I&+qbJ!RETT%E9(nq}KowB^0eSinwq}S1?QSxdTkdDH=~oN|8<l-'
            '{f@hC*DrKH$Hg${B-'
            '~E$^IKTW|TTMtJs+znA5>KRqWkLD{D_C;y<)`!t2D@7=f{;k4&XjPKuNF*FA*6HwXtAxeMxsyLPUI*Do^kKOXq*<'
            'akH|SDQ|_e;})p>|)OH6FFDk4aF<0%F55aqDHrobt2$%rBq&^h8(`ro!Y4@8_RX`htju5e?^{xAf9}g=j<P|_Pp)'
            'P8E+Xf+;%Y8oQ(hbz$#s8H01F^1A{1accRsHl@_E9G~93A8(d(0CE}9$PJ?w8@~k)t<IY~DULk7Tjv`xj8?Irvg`'
            'v95J=t!INTfD*PiI%{hC7Ey_uJNR@Kv5Uf!UxPO1(|;qjktZ?Df{(8wvJnD+b2*f{?BeL~z`TmZz9|!IGr7olN#$'
            'j1N!u_x8ufc1hAI{KpyJ?3tXO=_@|ZfA}kaOAg;1{4zdHe%n8NmApILKlPV0eQ+()M}5)N`J?EsVNaLr!gxcId`v'
            '5m*`iB@uFvN1249`9Ys*5U>}M^zMAqUYEohRm*0G%MeL*F1sB?_@zOU5ZU)+x{@xes6ndgPR1)9^W6FlCOh@zdX*'
            ')YnMQar}K2StDDsUIe;baonYK~OWR8)jQ~QiTSG#E;(dHL%oms|zI@#NYp{%Oakx766?Lfgmet&}2zkPx72f8AvX'
            'u@S>tB!P{8-(k-'
            'Im0opZUI4cs^w`Ehje=sSp7PWbV*1UD4d+k|e80C=(^r`3sd0+KKZ%S_$R#9Mv8J(9K3!xrs$Bg`No05&b*be%XD'
            'EC7rR?<ZPS~+Xg^?)QbK@3;g80^D$Zaz5URovF2){nZsT<xmZoVD(h`E_(0<apmzKFjekD_@ZiT5r}l@$fq-'
            'b#G8Ho0g4mYnrzQe;2$oy4)p(89je7Ivoj?!J3BV)mzFVfjcq}But0K6bL|E;Bj#)B)yLB;kt;Ix8~>K_j8et!Iu'
            '^!D!<+}_0*gS#x7c`LYj_-z371by2ND$Zfi^0p63O~!y5NTg-w3$wY$>(s=}S~77X5EZt0z~AbdCMX7oRAz-'
            '>p>x{^KG>J%Buh;^sU`d@*++S)uO?-g!iyUX*iwo{cbzH_!=-'
            'Y!G?M2C|V?#{10WT!tA5F|<Nhj$%zM`ZSAeIEWYez|`r7JFx-|3)Ej&TN&5t=2Xn>LSKpu-ef{aJ(NJqiNou=D2Q'
            '~O_H@2F8CN@5Li6a+IdjyMd$z9JSN8RZSHsK<gpYq>>Q^Eq@yL0%bSfGN09#WDM<vd|8?;;Cf)fqhc()RW0>;rB3'
            '5zH2SfzqL7<-EsSr6;Q8z~_4q@mm-jKb8<HHx6c4!x90o#<nr{>a@x~ae%AeE7%O}WS?{hmx1;!M#&@HHkD=S*mi'
            'J|;?Fk3lNV`Ct)i*eQUOLP`x?Zqux8#O;Iwe1J7{5i_cUUuDaAibhUj-'
            '8avrO~@n3e>sW%@Wht~Nlds0{U4Ui9(wy_C|h_?b>5Xx<Tc0Kl{*G1R~Ky@35T|E+D)X$sxO4MAvPHX7}DxC5y`j'
            's00|T?u50|gZ^S9HS^jA_3*$SLp?e==W$o1rUxab9z(U(F269<3!V#O}WKSERWZkcsXli5QIoU{8MVECvo0iK=m;'
            'S+#gf}6Y@RJfF!NYLX%y#}Ao`_w{5ZRF~d<4|8bm3O{#Ah+_W?zst^0k=FSM`+>P(yU;+hWp}ZGd`3X@;Jlg<zw;'
            'J?;T<kSM2;)71->$z!*Ui4|%$A=GKKDqy_Vs^W6u-'
            'gQj2gS(A&ZX#Aj3w+kdjVy^He4vZ6*2{U`^us|YW4fxbxbSTS4JKej8aE!^S%wgoj97493tx%Khw}N_`k#WQ_iAU'
            'Op{?7OypXNh(J%K*hX!biE^6E^+ASQT3Ho6Yb+vI{{kDr2Efcw8yu6jln{T+L0dsfd=dp7Pm))^ncqM~|YLw^|MT'
            '&g!Wqp70+R7Rh<2~SZgKl)(tilf5<#hvpBIfPN1J2C>-'
            'm7D}kc~QXC(ZjgP)^EBK;sINH!sG@f3)t}j<mks_RbD$`d@eN$Dhnj=<sZljVnDw9**j|K;wTi@3e<-'
            'aymYW)@R*z+OeUZk(5)0t_7KakgBf-'
            ';>iC%T{b9gz=@q33no`(S+A#ys*KfDd}*@?R3O}YYS6a#Gx?S!fT%>H%5OcoJpr5VZ}Hpaw|sh;p)BNF*SGrxSYI'
            '#lbY5N#g14{1U>HyH27W!jDCuSPOZiEpiCvZX#P!h}cHW|4xJ2IZy%*}TB~hcyYUA91Qs<vD%afu)dqFzE2o0q`n'
            '8;%cbRP@?%@sN+*+@_%hm`IN=fp%~+`8II6eQX;S_w+%2T$~`RN#JKXAY8MOklk}(y(XWw!(wP4H@RhOwgE}&n=g'
            'y&IcJvw9cNKf1yzG0W*t*8ggj;G`P_}dnUG?4dyV1X($;kom{nQ$eG!YvdVJ33%0Lwk;-'
            '%T?vfq%q71G}#TS_XQP7lXviWTsIk+v-'
            'PyHVU!2;~5wPJbTEin{1vFso1KYgFrEuIeiMHKw(wvpwSzB`<0i8sXF`nm4QE_t$wN-'
            '@I~c>^rN_Dz>PptZuy74BVeFJ;#8%J^{JT6R3egEHTYA00u}M{_>=gi-=H@adB$!NIG~(XR8AlB@9;7S;iZ`a?R-'
            'V>dHN@@*$~hmhSctDY+$<c)J)B~IBHatfkWD1B|^8ls9;G4V}WVG3WLrX~pY3yve$B_~5JMnRz5tfw|NY1G!AB7D'
            'ddTDmBixy7`0L?4~=I`%0UG6~w7rCsS=sVOf|H5duVboZiR@fekVhf--_C(dygOg4e7HA+va@J>nhGATT*tuRe&@'
            'GSda=`_GRt?OY6pBH>grGAyomwU3YsrGm%aXOtU>KOLg&JL#mqR)gO4dvQ@^X~NM-'
            '6<Wl90XSYei(|B!5AGqXs*F8Gfo+NK!=hho-Rj+qu0Nm?4Kluql2;R)S)D9j33gSv;Q_|>-K&$I)-'
            'jf$H&yYA>$d3Nx4|0J5mcxeJ6S_2a+RGr~_GuQQl|xkQq^)vmNC*Gq9#&^jrY6b0o*(z40-'
            'K?Qybya5R1~!r$J!I&g>Nz3;}%c2_~wX$I_9Q5=rkl{B)eEQO)9()=k2l<)D>9z+1BuEydC#bAh$@NZT1HSB3T;5'
            ';-'
            '*wpcYQbW$ZC+~%tqy%l_6r}x`#DznYCV_&Oh&^ev(ny#C&%8~}uUFdRz$hkp+nB~ssi>We?%=0+mnqhXMYTT~on('
            'M?3xmjP?H?s;+tSy2ERJty}D?ftNbB#J@e$`481%t(vEA5-;T37jPn&@pPz-nNd(UPB54B5C+PehX4L8?)?hgNuy'
            'tm$ig5v_akY{v*Ut#wRa+u`)Jhw&bMsE*svIUh=I7Wp$GDawpE$b_f|i6TB8wF62nzbtlyU3!&GuFb8QYF4!mSXt'
            't>ZiZp^;jL}Q?+Uwhr&rgCJD`<w#A}D;P5WRPa!rHj(V)Mn$Y=Z5f?8yyy3)uvDW@*_*fCPq(Bu7ue1i*>LIvT#O'
            'D(}AGIB(@ad}N>3nh*r0#lDF(`f+G;kqbq3N3fpxT1%M4qI1hw<?;ur^&*7yjxCH8hJcVSH%QxU^1N5RuovkvHjq'
            'xv2q9TxsgOsz^(9thnsh|ak#jC71(j!kkMzF!(@G8?Ve6=h9I$`FY3mhO%skP(i&6;LlCdky5&!BXH3DY`}f8B;#'
            'h_HOb{kQCk@z=X*K<2)ih-h{|?OguXPO$%dOzZW;XE!MTQ$NP)0aTeDVhtDM(@RfgY2(U-'
            '3q0H+b8KJ&_Y1g*gY?=_*G>A959Yy7Ze3>yW&2{2_*gDO!SoaM(R1vb8+QyQ-'
            '<AIZQk8TqrKpTwUh&9Y<6TLcrwLRFlNMKDhnfTgZU>mU9Y**_6>I44wsbmR6u@D8z^h0QJe#GGImS?9pv=g{P-'
            'KWs?=<u<izT^)1G@<pUXb)n5>61MJB)%ne=#EOEX?B}X{BAH8kRxzdmykcWnWUHWBBQv<d!2eEvO+oyii`hKLF0s'
            'uA7o_@08V_ua7u5=W?WI-8y8n0>IWs`e#-|+%$kS#ZTn)8%!!8}sm4l?RU73_#;>OhQp-qdzeJ04^E7RyZ`K86L0'
            'Ob`bTeb6#U$||8Hko;lHk+6&XYg0p!z95#3R9V3;yFiup*cC4y^{H8$QvK{BPMRMWp)<SqLPrJP;U*7%7u8H2GMq'
            'sauq4H@<_c_oSCNaTs=Tr05@4Ibq)zmAz@_EC^98+Ho!W<d+cy<&tP9X}u3KJ6*M0G=ZP+~8aJ5wHts5?4)hClI<'
            'ZK&HjdjCM*}G&FRM5%S#)m2!K^<~8AW8c`z4Mq32CS%MzX)%R^3d_!D3+cl7amv3BDvmn&6)?<X-'
            'd}=rcuRd3`<y+>S$MpWyvyh{?-'
            'kRlQBl@+ju(YedVDn&ta?<Gw9acmcM~scO%n0X(w<Q6DgCoOiAQPMq)_yYOzSGTgy0@iJ6Brq7O0Q@g=LW25-'
            '8=)uNp>K+M_~urs(b@VpOJxKTEWPj4-!?ql;3_+!|^RNb{LkVQ>2?!Ff{>V0n~I&7-'
            'w^8GZg`8&HJ2d@@E$mmN9Z_~KU3wC+p=!FZ~hzRh+P`;PwuGfP>B*gnkLh<z^L0ce6gm5LpAnN@uL%h6l'
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
        f"Unknown workflow operation {operation_key!r}. Available: {available}"
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
    dialog.setWindowTitle("RFPro Workflow")
    dialog.setMinimumWidth(520)
    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel("Choose an RFPro workflow operation:"))

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
            f"RFPro workflow operation {operation_key!r} is not embedded in this "
            "launcher. Update or regenerate rfpro_workflow.py."
        ) from error

    try:
        compressed = base64.b85decode(encoded_payload.encode("ascii"))
        source_bytes = zlib.decompress(compressed)
    except Exception as error:
        raise RuntimeError(
            f"Embedded RFPro workflow {filename!r} is corrupt and could not be "
            "decoded. Update the launcher from the repository."
        ) from error

    actual_digest = hashlib.sha256(source_bytes).hexdigest()
    if actual_digest != expected_digest:
        raise RuntimeError(
            f"Embedded RFPro workflow {filename!r} failed its integrity check: "
            f"expected {expected_digest}, got {actual_digest}."
        )
    return filename, source_bytes.decode("utf-8")


def load_embedded_tool_module(operation_key: str) -> tuple[str, Any]:
    """Load one bundled child as a registered in-memory Python module."""

    filename, source = embedded_tool_source(operation_key)
    module_name = f"_rfpro_workflow_embedded_{operation_key}"
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
        raise RuntimeError(f"Embedded RFPro workflow {filename!r} has no main().")
    child_main(list(arguments))


def run_operation(operation: Sequence[str], analysis_name: str) -> None:
    key, label, _description, filename = operation
    print(f"Launching embedded RFPro workflow: {label} ({filename})")
    execute_embedded_tool(key, ["--analysis", analysis_name])


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Combined RFPro workflow launcher.")
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
        print("RFPro workflow selection cancelled; nothing was run.")
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
            "RFPro workflow failed",
            f"{operation[1]} failed:\n\n{error}\n\n"
            "See the RFPro Python console for the complete traceback.",
        )
        raise


if __name__ == "__main__":
    main()
