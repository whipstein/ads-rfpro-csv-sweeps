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
