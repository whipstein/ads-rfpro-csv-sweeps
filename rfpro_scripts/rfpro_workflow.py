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
