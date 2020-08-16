import os
import recipeReader
import inspect
import xml.dom.minidom
import sys
import ctrl
import equipment
import appliances


def simpleBsmx():
    retval = """
<Recipes>
 <Name>Recipes</Name>
 <Data>
  <Recipe>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
   </F_R_MASH>
  </Recipe>
 </Data>
</Recipes>
    """
    return(retval)


def badMashProfile():
    retval = """
<Recipes>
 <Name>Recipes</Name>
 <Data>
  <Recipe>
   <F_R_NAME>BadProfile</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Bad Profile</F_MH_NAME>
   </F_R_MASH>
  </Recipe>
 </Data>
</Recipes>
    """
    return(retval)


def elaborateBsmx():
    retval = """
<Recipes>
 <Name>Recipes</Name>
 <Data>
  <Recipe>
   <F_R_NAME>18 Rune Stone  IPA 2.5G</F_R_NAME>
   <F_R_EQUIPMENT>
    <F_E_NAME>Grain 2.5G, 5Gcooler, 4Gpot</F_E_NAME>
    <F_E_MASH_VOL>640.0000000</F_E_MASH_VOL>
    <F_E_BOIL_VOL>436.7360000</F_E_BOIL_VOL>
   </F_R_EQUIPMENT>
   <F_R_MASH>
    <F_MH_NAME>Single Infusion, Medium Body, No Mash Out</F_MH_NAME>
    <F_MH_GRAIN_WEIGHT>116.0000000</F_MH_GRAIN_WEIGHT>
    <F_MH_GRAIN_TEMP>68.0000000</F_MH_GRAIN_TEMP>
   </F_R_MASH>
   <Data>
    <MashStep>
      <F_MS_NAME>Mash In</F_MS_NAME>
      <F_MS_INFUSION>290.0000000</F_MS_INFUSION>
      <F_MS_TUN_ADDITION>6.4000000</F_MS_TUN_ADDITION>
      <F_MS_STEP_TEMP>152.0000000</F_MS_STEP_TEMP>
      <F_MS_STEP_TIME>60.0000000</F_MS_STEP_TIME>
      <F_MS_GRAIN_WEIGHT>116.0000000</F_MS_GRAIN_WEIGHT>
      <F_MS_INFUSION>290.0000000</F_MS_INFUSION>
     </MashStep>
   </Data>
    <Ingredients>
     <Data>
      <Grain>
      </Grain>
      <Hops>
        <F_H_NAME>Columbus (Tomahawk)</F_H_NAME>
        <F_H_TYPE>0</F_H_TYPE>
        <F_H_FORM>0</F_H_FORM>
        <F_H_AMOUNT>1.0000000</F_H_AMOUNT>
        <F_H_BOIL_TIME>60.0000000</F_H_BOIL_TIME>
        <F_H_DRY_HOP_TIME>0.0000000</F_H_DRY_HOP_TIME>
        <F_H_IN_RECIPE>1</F_H_IN_RECIPE>
        <F_H_USE>0</F_H_USE>
      </Hops>
      <Misc>
        <F_M_NAME>Whirlfloc Tablet</F_M_NAME>
        <F_M_TYPE>1</F_M_TYPE>
        <F_M_USE_FOR>Clarity</F_M_USE_FOR>
        <F_M_TEMP_VOL>320.0000000</F_M_TEMP_VOL>
        <F_M_UNITS>13</F_M_UNITS>
        <F_M_AMOUNT>0.5000000</F_M_AMOUNT>
        <F_M_VOLUME>640.0000000</F_M_VOLUME>
        <F_M_USE>0</F_M_USE>
        <F_M_TIME_UNITS>0</F_M_TIME_UNITS>
        <F_M_TIME>15.0000000</F_M_TIME>
        <F_M_IMPORT_AS_WEIGHT>1</F_M_IMPORT_AS_WEIGHT>
        <F_M_IMPORT_UNITS>0</F_M_IMPORT_UNITS>
        <F_ORDER>4</F_ORDER>
      </Misc>
     </Data>
    </Ingredients>
  </Recipe>
 </Data>
</Recipes>
    """
    return(retval)


def badTunDeadSpaceBsmx():
    retval = """
<Recipes><_MOD_>1975-06-09</_MOD_>
<Name>Recipes</Name>
<Type>7372</Type>
<Owndata>0</Owndata>
<TID>123</TID>
<Size>1</Size>
<_XName>Recipes</_XName>
<Allocinc>16</Allocinc>
<Data><Recipe><_MOD_>2013-12-07</_MOD_>
<F_R_NAME>testcold</F_R_NAME>
<F_R_BREWER>mikael</F_R_BREWER>
<F_R_ASST_BREWER></F_R_ASST_BREWER>
<F_R_DATE>2013-02-02</F_R_DATE>
<F_R_INV_DATE>1992-02-01</F_R_INV_DATE>
<F_R_VOLUME_MEASURED>358.4000000</F_R_VOLUME_MEASURED>
<F_R_FINAL_VOL_MEASURED>307.2000000</F_R_FINAL_VOL_MEASURED>
<F_R_MASH_TIMER>0</F_R_MASH_TIMER>
<F_R_BOIL_TIMER>0</F_R_BOIL_TIMER>
<F_R_MTIMER_DOWN>0</F_R_MTIMER_DOWN>
<F_R_BTIMER_DOWN>0</F_R_BTIMER_DOWN>
<Image></Image>
<F_R_IMAGE_X>0</F_R_IMAGE_X>
<F_R_IMAGE_Y>0</F_R_IMAGE_Y>
<F_R_EQUIPMENT><_MOD_>2013-12-07</_MOD_>
<F_E_NAME>Grain 3G, 5Gcooler, 5Gpot</F_E_NAME>
<F_E_MASH_VOL>640.0000000</F_E_MASH_VOL>
<F_E_TUN_MASS>160.0000000</F_E_TUN_MASS>
<F_E_BOIL_RATE_FLAG>1</F_E_BOIL_RATE_FLAG>
<F_E_TUN_SPECIFIC_HEAT>0.3000000</F_E_TUN_SPECIFIC_HEAT>
<F_E_TUN_DEADSPACE>64.0000000</F_E_TUN_DEADSPACE>
<F_E_TUN_ADJ_DEADSPACE>1</F_E_TUN_ADJ_DEADSPACE>
<F_E_CALC_BOIL>1</F_E_CALC_BOIL>
<F_E_BOIL_VOL>183.7226667</F_E_BOIL_VOL>
<F_E_BOIL_TIME>10.0000000</F_E_BOIL_TIME>
<F_E_OLD_EVAP_RATE>10.0000000</F_E_OLD_EVAP_RATE>
<F_EQUIP_39>1</F_EQUIP_39>
<F_E_BOIL_OFF>64.0000000</F_E_BOIL_OFF>
<F_E_TRUB_LOSS>38.4000000</F_E_TRUB_LOSS>
<F_E_COOL_PCT>4.0000000</F_E_COOL_PCT>
<F_E_TOP_UP_KETTLE>0.0000000</F_E_TOP_UP_KETTLE>
<F_E_BATCH_VOL>128.0000000</F_E_BATCH_VOL>
<F_E_FERMENTER_LOSS>38.4000000</F_E_FERMENTER_LOSS>
<F_E_TOP_UP>0.0000000</F_E_TOP_UP>
<F_E_EFFICIENCY>58.0000000</F_E_EFFICIENCY>
<F_E_HOP_UTIL>100.0000000</F_E_HOP_UTIL>
<F_E_NOTES></F_E_NOTES>
</F_R_EQUIPMENT>
<F_R_STYLE><_MOD_>2013-11-24</_MOD_>
<F_S_NAME>California Common Beer</F_S_NAME>
<F_S_CATEGORY>Amber Hybrid Beer</F_S_CATEGORY>
<F_S_GUIDE>BJCP 2008</F_S_GUIDE>
<F_S_LETTER>2</F_S_LETTER>
<F_S_NUMBER>7</F_S_NUMBER>
<F_S_TYPE>2</F_S_TYPE>
<F_S_MIN_OG>1.0480000</F_S_MIN_OG>
<F_S_MAX_OG>1.0540000</F_S_MAX_OG>
<F_S_MIN_FG>1.0110000</F_S_MIN_FG>
<F_S_MAX_FG>1.0140000</F_S_MAX_FG>
<F_S_MIN_IBU>30.0000000</F_S_MIN_IBU>
<F_S_MAX_IBU>45.0000000</F_S_MAX_IBU>
<F_S_MIN_CARB>2.4000000</F_S_MIN_CARB>
<F_S_MAX_CARB>2.8000000</F_S_MAX_CARB>
<F_S_MIN_COLOR>10.0000000</F_S_MIN_COLOR>
<F_S_MAX_COLOR>14.0000000</F_S_MAX_COLOR>
<F_S_MIN_ABV>4.5000000</F_S_MIN_ABV>
<F_S_MAX_ABV>5.5000000</F_S_MAX_ABV>
<F_S_DESCRIPTION>A test program </F_S_DESCRIPTION>
<F_S_PROFILE>Aroma: Typical.</F_S_PROFILE>
<F_S_INGREDIENTS>Pale ale malt, </F_S_INGREDIENTS>
<F_S_EXAMPLES>Anchor Steam</F_S_EXAMPLES>
<F_S_WEB_LINK>http://www.bjcp.org</F_S_WEB_LINK>
</F_R_STYLE>
<F_R_MASH><_MOD_>2013-12-07</_MOD_>
<F_MH_NAME>testonly</F_MH_NAME>
<F_MH_GRAIN_WEIGHT>16.0000000</F_MH_GRAIN_WEIGHT>
<F_MH_GRAIN_TEMP>72.0000000</F_MH_GRAIN_TEMP>
<F_MH_BOIL_TEMP>212.0000000</F_MH_BOIL_TEMP>
<F_MH_TUN_TEMP>72.0000000</F_MH_TUN_TEMP>
<F_MH_PH>5.2000000</F_MH_PH>
<F_MH_SPARGE_TEMP>80.0000000</F_MH_SPARGE_TEMP>
<F_MH_BATCH>0</F_MH_BATCH>
<F_MH_BATCH_PCT>95.0000000</F_MH_BATCH_PCT>
<F_MH_BATCH_EVEN>1</F_MH_BATCH_EVEN>
<F_MH_BATCH_DRAIN>0</F_MH_BATCH_DRAIN>
<F_MASH_39>1</F_MASH_39>
<F_MH_TUN_DEADSPACE>64.0000000</F_MH_TUN_DEADSPACE>
<F_MH_BIAB_VOL>640.0000000</F_MH_BIAB_VOL>
<F_MH_BIAB>0</F_MH_BIAB>
<F_MH_NOTES>This is a mash to do a quicker test</F_MH_NOTES>
<steps><_MOD_>1975-11-11</_MOD_>
<Name>steps</Name>
<Type>7432</Type>
<Owndata>1</Owndata>
<TID>7149</TID>
<Size>1</Size>
<_XName>steps</_XName>
<Allocinc>16</Allocinc>
<Data><MashStep><_MOD_>2013-12-07</_MOD_>
<F_MS_NAME>Mash Step</F_MS_NAME>
<F_MS_TYPE>0</F_MS_TYPE>
<F_MS_INFUSION>0.0000000</F_MS_INFUSION>
<F_MS_STEP_TEMP>72.0000000</F_MS_STEP_TEMP>
<F_MS_STEP_TIME>2.0000000</F_MS_STEP_TIME>
<F_MS_RISE_TIME>4.0000000</F_MS_RISE_TIME>
<F_MS_TUN_ADDITION>0.0000000</F_MS_TUN_ADDITION>
<F_MS_TUN_HC>0.3000000</F_MS_TUN_HC>
<F_MS_TUN_VOL>640.0000000</F_MS_TUN_VOL>
<F_MS_TUN_TEMP>72.0000000</F_MS_TUN_TEMP>
<F_MS_TUN_MASS>160.0000000</F_MS_TUN_MASS>
<F_MS_START_TEMP>0.0000000</F_MS_START_TEMP>
<F_MS_GRAIN_TEMP>72.0000000</F_MS_GRAIN_TEMP>
<F_MS_START_VOL>0.0000000</F_MS_START_VOL>
<F_MS_GRAIN_WEIGHT>16.0000000</F_MS_GRAIN_WEIGHT>
<F_MS_INFUSION_TEMP>72.0000000</F_MS_INFUSION_TEMP>
<F_MS_DECOCTION_AMT>0.0000000</F_MS_DECOCTION_AMT>
</MashStep>
</Data>
<_TExpanded>1</_TExpanded>
</steps>
<F_MH_EQUIP_ADJUST>1</F_MH_EQUIP_ADJUST>
<F_MH_TUN_VOL>640.0000000</F_MH_TUN_VOL>
<F_MH_TUN_MASS>160.0000000</F_MH_TUN_MASS>
<F_MH_TUN_HC>0.3000000</F_MH_TUN_HC>
</F_R_MASH>
<F_R_BASE_GRAIN><_MOD_>2013-12-07</_MOD_>
<F_G_NAME>Malt</F_G_NAME>
<F_G_ORIGIN></F_G_ORIGIN>
<F_G_SUPPLIER></F_G_SUPPLIER>
<F_G_TYPE>0</F_G_TYPE>
<F_G_IN_RECIPE>0</F_G_IN_RECIPE>
<F_G_INVENTORY>0.0000000</F_G_INVENTORY>
<F_G_AMOUNT>16.0000000</F_G_AMOUNT>
<F_G_COLOR>3.0000000</F_G_COLOR>
<F_G_YIELD>75.0000000</F_G_YIELD>
<F_G_LATE_EXTRACT>0.0000000</F_G_LATE_EXTRACT>
<F_G_PERCENT>0.0000000</F_G_PERCENT>
<F_ORDER>0</F_ORDER>
<F_G_COARSE_FINE_DIFF>1.5000000</F_G_COARSE_FINE_DIFF>
<F_G_MOISTURE>4.0000000</F_G_MOISTURE>
<F_G_DIASTATIC_POWER>120.0000000</F_G_DIASTATIC_POWER>
<F_G_PROTEIN>11.7000000</F_G_PROTEIN>
<F_G_IBU_GAL_PER_LB>0.0000000</F_G_IBU_GAL_PER_LB>
<F_G_ADD_AFTER_BOIL>0</F_G_ADD_AFTER_BOIL>
<F_G_RECOMMEND_MASH>0</F_G_RECOMMEND_MASH>
<F_G_MAX_IN_BATCH>100.0000000</F_G_MAX_IN_BATCH>
<F_G_NOTES></F_G_NOTES>
<F_G_BOIL_TIME>60.0000000</F_G_BOIL_TIME>
<F_G_PRICE>1.5000000</F_G_PRICE>
<F_G_CONVERT_GRAIN></F_G_CONVERT_GRAIN>
</F_R_BASE_GRAIN>
<F_R_CARB><_MOD_>2013-12-07</_MOD_>
<F_C_NAME>Corn Sugar</F_C_NAME>
<F_C_TEMPERATURE>70.0000000</F_C_TEMPERATURE>
<F_C_TYPE>0</F_C_TYPE>
<F_C_PRIMER_NAME>Corn Sugar</F_C_PRIMER_NAME>
<F_C_CARB_RATE>100.0000000</F_C_CARB_RATE>
<F_C_NOTES>Use corn sugar for priming the beer</F_C_NOTES>
</F_R_CARB>
<F_R_AGE><_MOD_>2013-12-07</_MOD_>
<F_A_NAME>Ale, Two Stage</F_A_NAME>
<F_A_PRIM_TEMP>67.0000000</F_A_PRIM_TEMP>
<F_A_PRIM_END_TEMP>67.0000000</F_A_PRIM_END_TEMP>
<F_A_SEC_TEMP>67.0000000</F_A_SEC_TEMP>
<F_A_SEC_END_TEMP>67.0000000</F_A_SEC_END_TEMP>
<F_A_TERT_TEMP>65.0000000</F_A_TERT_TEMP>
<F_A_AGE_TEMP>65.0000000</F_A_AGE_TEMP>
<F_A_TERT_END_TEMP>65.0000000</F_A_TERT_END_TEMP>
<F_A_END_AGE_TEMP>65.0000000</F_A_END_AGE_TEMP>
<F_A_END_TEMPS_SET>1</F_A_END_TEMPS_SET>
<F_A_PRIM_DAYS>4.0000000</F_A_PRIM_DAYS>
<F_A_SEC_DAYS>10.0000000</F_A_SEC_DAYS>
<F_A_TERT_DAYS>7.0000000</F_A_TERT_DAYS>
<F_A_AGE>30.0000000</F_A_AGE>
<F_A_TYPE>1</F_A_TYPE>
<F_A_NOTES>Two stage ale fermentation</F_A_NOTES>
</F_R_AGE>
<Ingredients><_MOD_>1975-11-11</_MOD_>
<Name>New Folder</Name>
<Type>7405</Type>
<Owndata>1</Owndata>
<TID>7182</TID>
<Size>5</Size>
<_XName>Ingredients</_XName>
<Allocinc>16</Allocinc>
<Data><Grain><_MOD_>1975-06-02</_MOD_>
<F_G_NAME>American Pale Malt (2 Row) US</F_G_NAME>
<F_G_ORIGIN>US</F_G_ORIGIN>
<F_G_SUPPLIER> Great Western Malting Company</F_G_SUPPLIER>
<F_G_TYPE>0</F_G_TYPE>
<F_G_IN_RECIPE>1</F_G_IN_RECIPE>
<F_G_INVENTORY>0.0000000</F_G_INVENTORY>
<F_G_AMOUNT>16.0000000</F_G_AMOUNT>
<F_G_COLOR>2.8800000</F_G_COLOR>
<F_G_YIELD>79.0000000</F_G_YIELD>
<F_G_LATE_EXTRACT>0.0000000</F_G_LATE_EXTRACT>
<F_G_PERCENT>100.0000000</F_G_PERCENT>
<F_ORDER>1</F_ORDER>
<F_G_COARSE_FINE_DIFF>1.5000000</F_G_COARSE_FINE_DIFF>
<F_G_MOISTURE>3.9000000</F_G_MOISTURE>
<F_G_DIASTATIC_POWER>134.0000000</F_G_DIASTATIC_POWER>
<F_G_PROTEIN>12.5700000</F_G_PROTEIN>
<F_G_IBU_GAL_PER_LB>0.0000000</F_G_IBU_GAL_PER_LB>
<F_G_ADD_AFTER_BOIL>0</F_G_ADD_AFTER_BOIL>
<F_G_RECOMMEND_MASH>1</F_G_RECOMMEND_MASH>
<F_G_MAX_IN_BATCH>100.0000000</F_G_MAX_IN_BATCH>
<F_G_NOTES>Base malt for all beer styles
Moore Beer GR305</F_G_NOTES>
<F_G_BOIL_TIME>10.0000000</F_G_BOIL_TIME>
<F_G_PRICE>0.0718750</F_G_PRICE>
<F_G_CONVERT_GRAIN>Pale Liquid Extract</F_G_CONVERT_GRAIN>
</Grain>
<Hops><_MOD_>2014-01-14</_MOD_>
<F_H_NAME>Northern Brewer</F_H_NAME>
<F_H_ORIGIN>Germany</F_H_ORIGIN>
<F_H_TYPE>2</F_H_TYPE>
<F_H_FORM>0</F_H_FORM>
<F_H_ALPHA>8.5000000</F_H_ALPHA>
<F_H_BETA>4.0000000</F_H_BETA>
<F_H_PERCENT>50.0000000</F_H_PERCENT>
<F_H_INVENTORY>1.5006906</F_H_INVENTORY>
<F_H_AMOUNT>1.0000000</F_H_AMOUNT>
<F_H_HSI>35.0000000</F_H_HSI>
<F_H_BOIL_TIME>10.0000000</F_H_BOIL_TIME>
<F_H_DRY_HOP_TIME>3.0000000</F_H_DRY_HOP_TIME>
<F_H_NOTES>Also called Hallertauer Northern Brewers
Use for: Bittering and finishing both ales and lagers of all kinds
Aroma: Fine, dry, clean bittering hop.  Unique flavor.
Substitute: Hallertauer Mittelfrueh, Hallertauer
Examples: Anchor Steam, Old Peculiar, </F_H_NOTES>
<F_H_IBU_CONTRIB>59.2628151</F_H_IBU_CONTRIB>
<F_ORDER>2</F_ORDER>
<F_H_USE>0</F_H_USE>
<F_H_IN_RECIPE>1</F_H_IN_RECIPE>
<F_H_PRICE>1.0000000</F_H_PRICE>
</Hops>
<Misc><_MOD_>1987-03-22</_MOD_>
<F_M_NAME>Whirlfloc Tablet</F_M_NAME>
<F_M_TYPE>1</F_M_TYPE>
<F_M_USE_FOR>Clarity</F_M_USE_FOR>
<F_M_TEMP_VOL>384.0000000</F_M_TEMP_VOL>
<F_M_UNITS>13</F_M_UNITS>
<F_M_AMOUNT>1.0000000</F_M_AMOUNT>
<F_M_VOLUME>640.0000000</F_M_VOLUME>
<F_M_INVENTORY>12.0000000</F_M_INVENTORY>
<F_M_PRICE>0.1000000</F_M_PRICE>
<F_M_USE>0</F_M_USE>
<F_M_TIME_UNITS>0</F_M_TIME_UNITS>
<F_M_TIME>7.0000000</F_M_TIME>
<F_M_NOTES>Aids in clearing yeast and chill haze.</F_M_NOTES>
<F_M_IMPORT_AS_WEIGHT>1</F_M_IMPORT_AS_WEIGHT>
<F_M_IMPORT_UNITS>0</F_M_IMPORT_UNITS>
<F_ORDER>3</F_ORDER>
</Misc>
<Hops><_MOD_>1969-12-31</_MOD_>
<F_H_NAME>Northern Brewer</F_H_NAME>
<F_H_ORIGIN>Germany</F_H_ORIGIN>
<F_H_TYPE>2</F_H_TYPE>
<F_H_FORM>0</F_H_FORM>
<F_H_ALPHA>8.5000000</F_H_ALPHA>
<F_H_BETA>4.0000000</F_H_BETA>
<F_H_PERCENT>25.0000000</F_H_PERCENT>
<F_H_INVENTORY>0.5002302</F_H_INVENTORY>
<F_H_AMOUNT>0.5000000</F_H_AMOUNT>
<F_H_HSI>35.0000000</F_H_HSI>
<F_H_BOIL_TIME>5.0000000</F_H_BOIL_TIME>
<F_H_DRY_HOP_TIME>3.0000000</F_H_DRY_HOP_TIME>
<F_H_NOTES>Also called Hallertauer Northern Brewers
Use for: Bittering and finishing both ales and lagers of all kinds
Aroma: Fine, dry, clean bittering hop.  Unique flavor.
Substitute: Hallertauer Mittelfrueh, Hallertauer
Examples: Anchor Steam, Old Peculiar, </F_H_NOTES>
<F_H_IBU_CONTRIB>16.2923553</F_H_IBU_CONTRIB>
<F_ORDER>4</F_ORDER>
<F_H_USE>0</F_H_USE>
<F_H_IN_RECIPE>1</F_H_IN_RECIPE>
<F_H_PRICE>1.0000000</F_H_PRICE>
</Hops>
<Hops><_MOD_>1975-06-02</_MOD_>
<F_H_NAME>Northern Brewer</F_H_NAME>
<F_H_ORIGIN>Germany</F_H_ORIGIN>
<F_H_TYPE>2</F_H_TYPE>
<F_H_FORM>0</F_H_FORM>
<F_H_ALPHA>8.5000000</F_H_ALPHA>
<F_H_BETA>4.0000000</F_H_BETA>
<F_H_PERCENT>25.0000000</F_H_PERCENT>
<F_H_INVENTORY>0.0000000</F_H_INVENTORY>
<F_H_AMOUNT>0.5000000</F_H_AMOUNT>
<F_H_HSI>35.0000000</F_H_HSI>
<F_H_BOIL_TIME>0.0000000</F_H_BOIL_TIME>
<F_H_DRY_HOP_TIME>0.0000000</F_H_DRY_HOP_TIME>
<F_H_NOTES>Also called Hallertauer Northern Brewers
Used for: Bittering and finishing both ales and lagers of all kinds
Aroma: Fine, dry, clean bittering hop.  Unique flavor.
Substitutes: Hallertauer Mittelfrueh, Hallertauer
Examples: Anchor Steam, Old Peculiar, </F_H_NOTES>
<F_H_IBU_CONTRIB>0.0000000</F_H_IBU_CONTRIB>
<F_ORDER>5</F_ORDER>
<F_H_USE>0</F_H_USE>
<F_H_IN_RECIPE>1</F_H_IN_RECIPE>
<F_H_PRICE>1.0000000</F_H_PRICE>
</Hops>
</Data>
<_TExpanded>1</_TExpanded>
</Ingredients>
<F_R_TYPE>2</F_R_TYPE>
<F_R_OLD_TYPE>0</F_R_OLD_TYPE>
<F_R_LOCKED>0</F_R_LOCKED>
<F_R_OG_MEASURED>1.0520000</F_R_OG_MEASURED>
<F_R_FG_MEASURED>1.0120000</F_R_FG_MEASURED>
<F_R_OG_PRIMARY>1.0130000</F_R_OG_PRIMARY>
<F_R_OG_SECONDARY>0.0000000</F_R_OG_SECONDARY>
<F_R_BOIL_VOL_MEASURED>0.0000000</F_R_BOIL_VOL_MEASURED>
<F_R_OG_BOIL_MEASURED>0.0420000</F_R_OG_BOIL_MEASURED>
<F_R_NOTES>This is a dummy recipe to test the equipment.</F_R_NOTES>
<F_R_RATING>30.0000000</F_R_RATING>
<F_R_DESCRIPTION></F_R_DESCRIPTION>
<F_R_CARB_VOLS>2.4000000</F_R_CARB_VOLS>
<F_R_MASH_PH>5.2000000</F_R_MASH_PH>
<F_R_RUNOFF_PH>6.0000000</F_R_RUNOFF_PH>
<F_R_RUNNING_GRAVITY>1.0130000</F_R_RUNNING_GRAVITY>
<F_R_GRAIN_STEEP_TIME>30</F_R_GRAIN_STEEP_TIME>
<F_R_GRAIN_STEEP_TEMP>155.0000000</F_R_GRAIN_STEEP_TEMP>
<F_R_INCLUDE_STARTER>1</F_R_INCLUDE_STARTER>
<F_R_VERSION>1.0000000</F_R_VERSION>
<F_R_STARTER_SIZE>33.8138278</F_R_STARTER_SIZE>
<F_R_STIR_PLATE>0</F_R_STIR_PLATE>
<F_R_OLD_VOL>320.0000000</F_R_OLD_VOL>
<F_R_OLD_BOIL_VOL>396.8000000</F_R_OLD_BOIL_VOL>
<F_R_OLD_EFFICIENCY>55.0000000</F_R_OLD_EFFICIENCY>
<F_R_DESIRED_IBU>20.0000000</F_R_DESIRED_IBU>
<F_R_DESIRED_COLOR>10.0000000</F_R_DESIRED_COLOR>
<F_R_COLOR_ADJ_STRING></F_R_COLOR_ADJ_STRING>
<F_R_DESIRED_OG>1.0500000</F_R_DESIRED_OG>
<F_R_REBALANCE_SCALE>1</F_R_REBALANCE_SCALE>
</Recipe>
</Data>
<_TExpanded>1</_TExpanded>
</Recipes>
    """
    return(retval)


def goodRecipe():
    retval = """
<Recipes><_MOD_>1975-06-09</_MOD_>
<Name>Recipes</Name>
<Type>7372</Type>
<Owndata>0</Owndata>
<TID>123</TID>
<Size>1</Size>
<_XName>Recipes</_XName>
<Allocinc>16</Allocinc>
<Data><Recipe><_MOD_>2013-12-07</_MOD_>
<F_R_NAME>testcold</F_R_NAME>
<F_R_BREWER>mikael</F_R_BREWER>
<F_R_ASST_BREWER></F_R_ASST_BREWER>
<F_R_DATE>2013-02-02</F_R_DATE>
<F_R_INV_DATE>1992-02-01</F_R_INV_DATE>
<F_R_VOLUME_MEASURED>358.4000000</F_R_VOLUME_MEASURED>
<F_R_FINAL_VOL_MEASURED>307.2000000</F_R_FINAL_VOL_MEASURED>
<F_R_MASH_TIMER>0</F_R_MASH_TIMER>
<F_R_BOIL_TIMER>0</F_R_BOIL_TIMER>
<F_R_MTIMER_DOWN>0</F_R_MTIMER_DOWN>
<F_R_BTIMER_DOWN>0</F_R_BTIMER_DOWN>
<Image></Image>
<F_R_IMAGE_X>0</F_R_IMAGE_X>
<F_R_IMAGE_Y>0</F_R_IMAGE_Y>
<F_R_EQUIPMENT><_MOD_>2013-12-07</_MOD_>
<F_E_NAME>Grain 3G, 5Gcooler, 5Gpot</F_E_NAME>
<F_E_MASH_VOL>640.0000000</F_E_MASH_VOL>
<F_E_TUN_MASS>160.0000000</F_E_TUN_MASS>
<F_E_BOIL_RATE_FLAG>1</F_E_BOIL_RATE_FLAG>
<F_E_TUN_SPECIFIC_HEAT>0.3000000</F_E_TUN_SPECIFIC_HEAT>
<F_E_TUN_DEADSPACE>64.0000000</F_E_TUN_DEADSPACE>
<F_E_TUN_ADJ_DEADSPACE>1</F_E_TUN_ADJ_DEADSPACE>
<F_E_CALC_BOIL>1</F_E_CALC_BOIL>
<F_E_BOIL_VOL>183.7226667</F_E_BOIL_VOL>
<F_E_BOIL_TIME>10.0000000</F_E_BOIL_TIME>
<F_E_OLD_EVAP_RATE>10.0000000</F_E_OLD_EVAP_RATE>
<F_EQUIP_39>1</F_EQUIP_39>
<F_E_BOIL_OFF>64.0000000</F_E_BOIL_OFF>
<F_E_TRUB_LOSS>38.4000000</F_E_TRUB_LOSS>
<F_E_COOL_PCT>4.0000000</F_E_COOL_PCT>
<F_E_TOP_UP_KETTLE>0.0000000</F_E_TOP_UP_KETTLE>
<F_E_BATCH_VOL>128.0000000</F_E_BATCH_VOL>
<F_E_FERMENTER_LOSS>38.4000000</F_E_FERMENTER_LOSS>
<F_E_TOP_UP>0.0000000</F_E_TOP_UP>
<F_E_EFFICIENCY>58.0000000</F_E_EFFICIENCY>
<F_E_HOP_UTIL>100.0000000</F_E_HOP_UTIL>
<F_E_NOTES></F_E_NOTES>
</F_R_EQUIPMENT>
<F_R_STYLE><_MOD_>2013-11-24</_MOD_>
<F_S_NAME>California Common Beer</F_S_NAME>
<F_S_CATEGORY>Amber Hybrid Beer</F_S_CATEGORY>
<F_S_GUIDE>BJCP 2008</F_S_GUIDE>
<F_S_LETTER>2</F_S_LETTER>
<F_S_NUMBER>7</F_S_NUMBER>
<F_S_TYPE>2</F_S_TYPE>
<F_S_MIN_OG>1.0480000</F_S_MIN_OG>
<F_S_MAX_OG>1.0540000</F_S_MAX_OG>
<F_S_MIN_FG>1.0110000</F_S_MIN_FG>
<F_S_MAX_FG>1.0140000</F_S_MAX_FG>
<F_S_MIN_IBU>30.0000000</F_S_MIN_IBU>
<F_S_MAX_IBU>45.0000000</F_S_MAX_IBU>
<F_S_MIN_CARB>2.4000000</F_S_MIN_CARB>
<F_S_MAX_CARB>2.8000000</F_S_MAX_CARB>
<F_S_MIN_COLOR>10.0000000</F_S_MIN_COLOR>
<F_S_MAX_COLOR>14.0000000</F_S_MAX_COLOR>
<F_S_MIN_ABV>4.5000000</F_S_MIN_ABV>
<F_S_MAX_ABV>5.5000000</F_S_MAX_ABV>
<F_S_DESCRIPTION>A lightly fruity beer</F_S_DESCRIPTION>
<F_S_PROFILE>Aroma: Typical.</F_S_PROFILE>
<F_S_INGREDIENTS>Pale ale malt</F_S_INGREDIENTS>
<F_S_EXAMPLES>Anchor Steam</F_S_EXAMPLES>
<F_S_WEB_LINK>http://www.bjcp.org</F_S_WEB_LINK>
</F_R_STYLE>
<F_R_MASH><_MOD_>2013-12-07</_MOD_>
<F_MH_NAME>testonly</F_MH_NAME>
<F_MH_GRAIN_WEIGHT>16.0000000</F_MH_GRAIN_WEIGHT>
<F_MH_GRAIN_TEMP>72.0000000</F_MH_GRAIN_TEMP>
<F_MH_BOIL_TEMP>212.0000000</F_MH_BOIL_TEMP>
<F_MH_TUN_TEMP>72.0000000</F_MH_TUN_TEMP>
<F_MH_PH>5.2000000</F_MH_PH>
<F_MH_SPARGE_TEMP>80.0000000</F_MH_SPARGE_TEMP>
<F_MH_BATCH>0</F_MH_BATCH>
<F_MH_BATCH_PCT>95.0000000</F_MH_BATCH_PCT>
<F_MH_BATCH_EVEN>1</F_MH_BATCH_EVEN>
<F_MH_BATCH_DRAIN>0</F_MH_BATCH_DRAIN>
<F_MASH_39>1</F_MASH_39>
<F_MH_TUN_DEADSPACE>64.0000000</F_MH_TUN_DEADSPACE>
<F_MH_BIAB_VOL>640.0000000</F_MH_BIAB_VOL>
<F_MH_BIAB>0</F_MH_BIAB>
<F_MH_NOTES>This is a mash to do a quicker test</F_MH_NOTES>
<steps><_MOD_>1975-11-11</_MOD_>
<Name>steps</Name>
<Type>7432</Type>
<Owndata>1</Owndata>
<TID>7149</TID>
<Size>1</Size>
<_XName>steps</_XName>
<Allocinc>16</Allocinc>
<Data><MashStep><_MOD_>2013-12-07</_MOD_>
<F_MS_NAME>Mash Step</F_MS_NAME>
<F_MS_TYPE>0</F_MS_TYPE>
<F_MS_INFUSION>0.0000000</F_MS_INFUSION>
<F_MS_STEP_TEMP>72.0000000</F_MS_STEP_TEMP>
<F_MS_STEP_TIME>2.0000000</F_MS_STEP_TIME>
<F_MS_RISE_TIME>4.0000000</F_MS_RISE_TIME>
<F_MS_TUN_ADDITION>64.0000000</F_MS_TUN_ADDITION>
<F_MS_TUN_HC>0.3000000</F_MS_TUN_HC>
<F_MS_TUN_VOL>640.0000000</F_MS_TUN_VOL>
<F_MS_TUN_TEMP>72.0000000</F_MS_TUN_TEMP>
<F_MS_TUN_MASS>160.0000000</F_MS_TUN_MASS>
<F_MS_START_TEMP>0.0000000</F_MS_START_TEMP>
<F_MS_GRAIN_TEMP>72.0000000</F_MS_GRAIN_TEMP>
<F_MS_START_VOL>0.0000000</F_MS_START_VOL>
<F_MS_GRAIN_WEIGHT>16.0000000</F_MS_GRAIN_WEIGHT>
<F_MS_INFUSION_TEMP>72.0000000</F_MS_INFUSION_TEMP>
<F_MS_DECOCTION_AMT>0.0000000</F_MS_DECOCTION_AMT>
</MashStep>
</Data>
<_TExpanded>1</_TExpanded>
</steps>
<F_MH_EQUIP_ADJUST>1</F_MH_EQUIP_ADJUST>
<F_MH_TUN_VOL>640.0000000</F_MH_TUN_VOL>
<F_MH_TUN_MASS>160.0000000</F_MH_TUN_MASS>
<F_MH_TUN_HC>0.3000000</F_MH_TUN_HC>
</F_R_MASH>
<F_R_BASE_GRAIN><_MOD_>2013-12-07</_MOD_>
<F_G_NAME>Malt</F_G_NAME>
<F_G_ORIGIN></F_G_ORIGIN>
<F_G_SUPPLIER></F_G_SUPPLIER>
<F_G_TYPE>0</F_G_TYPE>
<F_G_IN_RECIPE>0</F_G_IN_RECIPE>
<F_G_INVENTORY>0.0000000</F_G_INVENTORY>
<F_G_AMOUNT>16.0000000</F_G_AMOUNT>
<F_G_COLOR>3.0000000</F_G_COLOR>
<F_G_YIELD>75.0000000</F_G_YIELD>
<F_G_LATE_EXTRACT>0.0000000</F_G_LATE_EXTRACT>
<F_G_PERCENT>0.0000000</F_G_PERCENT>
<F_ORDER>0</F_ORDER>
<F_G_COARSE_FINE_DIFF>1.5000000</F_G_COARSE_FINE_DIFF>
<F_G_MOISTURE>4.0000000</F_G_MOISTURE>
<F_G_DIASTATIC_POWER>120.0000000</F_G_DIASTATIC_POWER>
<F_G_PROTEIN>11.7000000</F_G_PROTEIN>
<F_G_IBU_GAL_PER_LB>0.0000000</F_G_IBU_GAL_PER_LB>
<F_G_ADD_AFTER_BOIL>0</F_G_ADD_AFTER_BOIL>
<F_G_RECOMMEND_MASH>0</F_G_RECOMMEND_MASH>
<F_G_MAX_IN_BATCH>100.0000000</F_G_MAX_IN_BATCH>
<F_G_NOTES></F_G_NOTES>
<F_G_BOIL_TIME>60.0000000</F_G_BOIL_TIME>
<F_G_PRICE>1.5000000</F_G_PRICE>
<F_G_CONVERT_GRAIN></F_G_CONVERT_GRAIN>
</F_R_BASE_GRAIN>
<F_R_CARB><_MOD_>2013-12-07</_MOD_>
<F_C_NAME>Corn Sugar</F_C_NAME>
<F_C_TEMPERATURE>70.0000000</F_C_TEMPERATURE>
<F_C_TYPE>0</F_C_TYPE>
<F_C_PRIMER_NAME>Corn Sugar</F_C_PRIMER_NAME>
<F_C_CARB_RATE>100.0000000</F_C_CARB_RATE>
<F_C_NOTES>Use corn sugar for priming the beer</F_C_NOTES>
</F_R_CARB>
<F_R_AGE><_MOD_>2013-12-07</_MOD_>
<F_A_NAME>Ale, Two Stage</F_A_NAME>
<F_A_PRIM_TEMP>67.0000000</F_A_PRIM_TEMP>
<F_A_PRIM_END_TEMP>67.0000000</F_A_PRIM_END_TEMP>
<F_A_SEC_TEMP>67.0000000</F_A_SEC_TEMP>
<F_A_SEC_END_TEMP>67.0000000</F_A_SEC_END_TEMP>
<F_A_TERT_TEMP>65.0000000</F_A_TERT_TEMP>
<F_A_AGE_TEMP>65.0000000</F_A_AGE_TEMP>
<F_A_TERT_END_TEMP>65.0000000</F_A_TERT_END_TEMP>
<F_A_END_AGE_TEMP>65.0000000</F_A_END_AGE_TEMP>
<F_A_END_TEMPS_SET>1</F_A_END_TEMPS_SET>
<F_A_PRIM_DAYS>4.0000000</F_A_PRIM_DAYS>
<F_A_SEC_DAYS>10.0000000</F_A_SEC_DAYS>
<F_A_TERT_DAYS>7.0000000</F_A_TERT_DAYS>
<F_A_AGE>30.0000000</F_A_AGE>
<F_A_TYPE>1</F_A_TYPE>
<F_A_NOTES>Two stage ale.</F_A_NOTES>
</F_R_AGE>
<Ingredients><_MOD_>1975-11-11</_MOD_>
<Name>New Folder</Name>
<Type>7405</Type>
<Owndata>1</Owndata>
<TID>7182</TID>
<Size>5</Size>
<_XName>Ingredients</_XName>
<Allocinc>16</Allocinc>
<Data><Grain><_MOD_>1975-06-02</_MOD_>
<F_G_NAME>American Pale Malt (2 Row) US</F_G_NAME>
<F_G_ORIGIN>US</F_G_ORIGIN>
<F_G_SUPPLIER> Great Western Malting Company</F_G_SUPPLIER>
<F_G_TYPE>0</F_G_TYPE>
<F_G_IN_RECIPE>1</F_G_IN_RECIPE>
<F_G_INVENTORY>0.0000000</F_G_INVENTORY>
<F_G_AMOUNT>16.0000000</F_G_AMOUNT>
<F_G_COLOR>2.8800000</F_G_COLOR>
<F_G_YIELD>79.0000000</F_G_YIELD>
<F_G_LATE_EXTRACT>0.0000000</F_G_LATE_EXTRACT>
<F_G_PERCENT>100.0000000</F_G_PERCENT>
<F_ORDER>1</F_ORDER>
<F_G_COARSE_FINE_DIFF>1.5000000</F_G_COARSE_FINE_DIFF>
<F_G_MOISTURE>3.9000000</F_G_MOISTURE>
<F_G_DIASTATIC_POWER>134.0000000</F_G_DIASTATIC_POWER>
<F_G_PROTEIN>12.5700000</F_G_PROTEIN>
<F_G_IBU_GAL_PER_LB>0.0000000</F_G_IBU_GAL_PER_LB>
<F_G_ADD_AFTER_BOIL>0</F_G_ADD_AFTER_BOIL>
<F_G_RECOMMEND_MASH>1</F_G_RECOMMEND_MASH>
<F_G_MAX_IN_BATCH>100.0000000</F_G_MAX_IN_BATCH>
<F_G_NOTES>Base malt for all beer styles
Moore Beer GR305</F_G_NOTES>
<F_G_BOIL_TIME>10.0000000</F_G_BOIL_TIME>
<F_G_PRICE>0.0718750</F_G_PRICE>
<F_G_CONVERT_GRAIN>Pale Liquid Extract</F_G_CONVERT_GRAIN>
</Grain>
<Hops><_MOD_>2014-01-14</_MOD_>
<F_H_NAME>Northern Brewer</F_H_NAME>
<F_H_ORIGIN>Germany</F_H_ORIGIN>
<F_H_TYPE>2</F_H_TYPE>
<F_H_FORM>0</F_H_FORM>
<F_H_ALPHA>8.5000000</F_H_ALPHA>
<F_H_BETA>4.0000000</F_H_BETA>
<F_H_PERCENT>50.0000000</F_H_PERCENT>
<F_H_INVENTORY>1.5006906</F_H_INVENTORY>
<F_H_AMOUNT>1.0000000</F_H_AMOUNT>
<F_H_HSI>35.0000000</F_H_HSI>
<F_H_BOIL_TIME>10.0000000</F_H_BOIL_TIME>
<F_H_DRY_HOP_TIME>3.0000000</F_H_DRY_HOP_TIME>
<F_H_NOTES>Also called Hallertauer Northern Brewers
Use for: Bittering and finishing both ales and lagers of all kinds
Aroma: Fine, dry, clean bittering hop.  Unique flavor.
Substitute: Hallertauer Mittelfrueh, Hallertauer
Examples: Anchor Steam, Old Peculiar, </F_H_NOTES>
<F_H_IBU_CONTRIB>59.2628151</F_H_IBU_CONTRIB>
<F_ORDER>2</F_ORDER>
<F_H_USE>0</F_H_USE>
<F_H_IN_RECIPE>1</F_H_IN_RECIPE>
<F_H_PRICE>1.0000000</F_H_PRICE>
</Hops>
<Misc><_MOD_>1987-03-22</_MOD_>
<F_M_NAME>Whirlfloc Tablet</F_M_NAME>
<F_M_TYPE>1</F_M_TYPE>
<F_M_USE_FOR>Clarity</F_M_USE_FOR>
<F_M_TEMP_VOL>384.0000000</F_M_TEMP_VOL>
<F_M_UNITS>13</F_M_UNITS>
<F_M_AMOUNT>1.0000000</F_M_AMOUNT>
<F_M_VOLUME>640.0000000</F_M_VOLUME>
<F_M_INVENTORY>12.0000000</F_M_INVENTORY>
<F_M_PRICE>0.1000000</F_M_PRICE>
<F_M_USE>0</F_M_USE>
<F_M_TIME_UNITS>0</F_M_TIME_UNITS>
<F_M_TIME>7.0000000</F_M_TIME>
<F_M_NOTES>Aids in clearing yeast and chill haze.</F_M_NOTES>
<F_M_IMPORT_AS_WEIGHT>1</F_M_IMPORT_AS_WEIGHT>
<F_M_IMPORT_UNITS>0</F_M_IMPORT_UNITS>
<F_ORDER>3</F_ORDER>
</Misc>
<Hops><_MOD_>1969-12-31</_MOD_>
<F_H_NAME>Northern Brewer</F_H_NAME>
<F_H_ORIGIN>Germany</F_H_ORIGIN>
<F_H_TYPE>2</F_H_TYPE>
<F_H_FORM>0</F_H_FORM>
<F_H_ALPHA>8.5000000</F_H_ALPHA>
<F_H_BETA>4.0000000</F_H_BETA>
<F_H_PERCENT>25.0000000</F_H_PERCENT>
<F_H_INVENTORY>0.5002302</F_H_INVENTORY>
<F_H_AMOUNT>0.5000000</F_H_AMOUNT>
<F_H_HSI>35.0000000</F_H_HSI>
<F_H_BOIL_TIME>5.0000000</F_H_BOIL_TIME>
<F_H_DRY_HOP_TIME>3.0000000</F_H_DRY_HOP_TIME>
<F_H_NOTES>Also called Hallertauer Northern Brewers
Use for: Bittering and finishing both ales and lagers of all kinds
Aroma: Fine, dry, clean bittering hop.  Unique flavor.
Substitute: Hallertauer Mittelfrueh, Hallertauer
Examples: Anchor Steam, Old Peculiar, </F_H_NOTES>
<F_H_IBU_CONTRIB>16.2923553</F_H_IBU_CONTRIB>
<F_ORDER>4</F_ORDER>
<F_H_USE>0</F_H_USE>
<F_H_IN_RECIPE>1</F_H_IN_RECIPE>
<F_H_PRICE>1.0000000</F_H_PRICE>
</Hops>
<Hops><_MOD_>1975-06-02</_MOD_>
<F_H_NAME>Northern Brewer</F_H_NAME>
<F_H_ORIGIN>Germany</F_H_ORIGIN>
<F_H_TYPE>2</F_H_TYPE>
<F_H_FORM>0</F_H_FORM>
<F_H_ALPHA>8.5000000</F_H_ALPHA>
<F_H_BETA>4.0000000</F_H_BETA>
<F_H_PERCENT>25.0000000</F_H_PERCENT>
<F_H_INVENTORY>0.0000000</F_H_INVENTORY>
<F_H_AMOUNT>0.5000000</F_H_AMOUNT>
<F_H_HSI>35.0000000</F_H_HSI>
<F_H_BOIL_TIME>0.0000000</F_H_BOIL_TIME>
<F_H_DRY_HOP_TIME>0.0000000</F_H_DRY_HOP_TIME>
<F_H_NOTES>Also called Hallertauer Northern Brewers
Used for: Bittering and finishing both ales and lagers of all kinds
Aroma: Fine, dry, clean bittering hop.  Unique flavor.
Substitutes: Hallertauer Mittelfrueh, Hallertauer
Examples: Anchor Steam, Old Peculiar, </F_H_NOTES>
<F_H_IBU_CONTRIB>0.0000000</F_H_IBU_CONTRIB>
<F_ORDER>5</F_ORDER>
<F_H_USE>0</F_H_USE>
<F_H_IN_RECIPE>1</F_H_IN_RECIPE>
<F_H_PRICE>1.0000000</F_H_PRICE>
</Hops>
</Data>
<_TExpanded>1</_TExpanded>
</Ingredients>
<F_R_TYPE>2</F_R_TYPE>
<F_R_OLD_TYPE>0</F_R_OLD_TYPE>
<F_R_LOCKED>0</F_R_LOCKED>
<F_R_OG_MEASURED>1.0520000</F_R_OG_MEASURED>
<F_R_FG_MEASURED>1.0120000</F_R_FG_MEASURED>
<F_R_OG_PRIMARY>1.0130000</F_R_OG_PRIMARY>
<F_R_OG_SECONDARY>0.0000000</F_R_OG_SECONDARY>
<F_R_BOIL_VOL_MEASURED>0.0000000</F_R_BOIL_VOL_MEASURED>
<F_R_OG_BOIL_MEASURED>0.0420000</F_R_OG_BOIL_MEASURED>
<F_R_NOTES>This is a dummy recipe to test the equipment.</F_R_NOTES>
<F_R_RATING>30.0000000</F_R_RATING>
<F_R_DESCRIPTION></F_R_DESCRIPTION>
<F_R_CARB_VOLS>2.4000000</F_R_CARB_VOLS>
<F_R_MASH_PH>5.2000000</F_R_MASH_PH>
<F_R_RUNOFF_PH>6.0000000</F_R_RUNOFF_PH>
<F_R_RUNNING_GRAVITY>1.0130000</F_R_RUNNING_GRAVITY>
<F_R_GRAIN_STEEP_TIME>30</F_R_GRAIN_STEEP_TIME>
<F_R_GRAIN_STEEP_TEMP>155.0000000</F_R_GRAIN_STEEP_TEMP>
<F_R_INCLUDE_STARTER>1</F_R_INCLUDE_STARTER>
<F_R_VERSION>1.0000000</F_R_VERSION>
<F_R_STARTER_SIZE>33.8138278</F_R_STARTER_SIZE>
<F_R_STIR_PLATE>0</F_R_STIR_PLATE>
<F_R_OLD_VOL>320.0000000</F_R_OLD_VOL>
<F_R_OLD_BOIL_VOL>396.8000000</F_R_OLD_BOIL_VOL>
<F_R_OLD_EFFICIENCY>55.0000000</F_R_OLD_EFFICIENCY>
<F_R_DESIRED_IBU>20.0000000</F_R_DESIRED_IBU>
<F_R_DESIRED_COLOR>10.0000000</F_R_DESIRED_COLOR>
<F_R_COLOR_ADJ_STRING></F_R_COLOR_ADJ_STRING>
<F_R_DESIRED_OG>1.0500000</F_R_DESIRED_OG>
<F_R_REBALANCE_SCALE>1</F_R_REBALANCE_SCALE>
</Recipe>
</Data>
<_TExpanded>1</_TExpanded>
</Recipes>
"""
    return(retval)


def ctrlBsmxList():
    retlst = ctrl.controllerList()
    retlst.addController('controllerInfo', appliances.controllerinfo())
    retlst.addController('wortPump', appliances.wortPump())
    retlst.addController('boiler', appliances.boiler())
    #retlst = ['wortPump', 'boiler']
    return(retlst)


def txDocFromString(bsmxStr):
    """
    Creates doc from an xml string
    """
    bsmxCleanData = bsmxStr.replace('&', 'AMP')
    return(xml.dom.minidom.parseString(bsmxCleanData))


def test_init_bsmxStages_string():
    bx = recipeReader.bsmxStages(simpleBsmx(), ctrlBsmxList())
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    assert equipmentName == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getEquipment() == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getStages() == {}
    print(myname(), "OK")


def test_badProfile():
    bx = recipeReader.bsmxStages(badMashProfile(), ctrlBsmxList())
    assert bx.getRecipeName() == "BadProfile"
    doc = bx.getDocTree()
    profileName = recipeReader.bsmxReadString(doc, "F_R_NAME")
    print(profileName)
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    print(equipmentName)
    assert equipmentName == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getEquipment() == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getStages() == {}
    print(myname(), "OK")


def test_init_bsmxStages_file():
    cp = os.path.dirname(__file__)
    print(cp)
    rp = cp + "/../../beersmith/18RuneStoneIPA.bsmx"
    print(rp)
    e = equipment.allEquipment()
    myequipment = e.get("Grain 2.5G, 5Gcooler, 4Gpot")
    ctrl = ctrlBsmxList()
    ctrl['controllerInfo'].setEquipment(myequipment)
    print(ctrl['controllerInfo'].getEquipmentName())
    bx = recipeReader.bsmxStages(rp, ctrl)
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    assert equipmentName == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getEquipment() == "Grain 2.5G, 5Gcooler, 4Gpot"
    #print bx.getStages()
    assert bx.getStages() != {}
    print(myname(), "OK")


def test_init_bsmxStages_doc():
    doc = txDocFromString(simpleBsmx())
    bx = recipeReader.bsmxStages(doc, ctrlBsmxList())
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    assert equipmentName == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getEquipment() == "Grain 2.5G, 5Gcooler, 4Gpot"
    assert bx.getStages() == {}
    print(myname(), "OK")


def test_testcold():
    cp = os.path.dirname(__file__)
    print(cp)
    rp = cp + "/../../beersmith/testcold.bsmx"
    print(rp)
    e = equipment.allEquipment()
    myequipment = e.get("Grain 3G, 5Gcooler, 5Gpot")
    ctrl = ctrlBsmxList()
    ctrl['controllerInfo'].setEquipment(myequipment)
    print(ctrl['controllerInfo'].getEquipmentName())
    bx = recipeReader.bsmxStages(rp, ctrl)
    assert bx.getRecipeName() == "testcold"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    print(equipmentName)
    assert equipmentName == "Grain 3G, 5Gcooler, 5Gpot"
    assert bx.getEquipment() == "Grain 3G, 5Gcooler, 5Gpot"
    #print bx.getStages()
    assert bx.getStages() != {}
    print(myname(), "OK")


def test_testbatchsparge():
    cp = os.path.dirname(__file__)
    print(cp)
    rp = cp + "/../../beersmith/SilverDollarPorter.bsmx"
    print(rp)
    e = equipment.allEquipment()
    myequipment = e.get("Pot and Cooler ( 5 Gal/19 L) - All Grain")
    ctrl = ctrlBsmxList()
    ctrl['controllerInfo'].setEquipment(myequipment)
    print(ctrl['controllerInfo'].getEquipmentName())
    bx = recipeReader.bsmxStages(rp, ctrl)
    print(bx.getRecipeName())
    assert bx.getRecipeName() == "Silver Dollar Porter 2.5 gallons"
    doc = bx.getDocTree()
    equipmentName = recipeReader.bsmxReadString(doc, "F_E_NAME")
    print(equipmentName)
    assert equipmentName == "Pot and Cooler ( 5 Gal/19 L) - All Grain"
    assert bx.getEquipment() == "Pot and Cooler ( 5 Gal/19 L) - All Grain"
    #print bx.getStages()
    assert bx.getStages() != {}
    print(myname(), "OK")


def test_getFieldStr():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    v = bx.getFieldStr('F_E_MASH_VOL')
    assert isinstance(v, str) or isinstance(v, unicode)
    assert v == '640.0000000'
    print(myname(), "OK")


def test_getVolG():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    v = bx.getVolG('F_E_MASH_VOL')
    assert isinstance(v, float)
    assert abs(v - 5.0) < 0.1
    print(myname(), "OK")


def test_GoodRecipe():
    print(os.getcwd())
    e = equipment.allEquipment('src/equipment/*.yaml')
    myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot')
    bx = recipeReader.bsmxStages(goodRecipe(),
                                 ctrl.setupControllers(False, True, True, myequipment))
    assert bx.isValid()
    print(myname(), "OK")


def test_badTunDeadSpace():
    print(os.getcwd())
    e = equipment.allEquipment('src/equipment/*.yaml')
    myequipment = e.get('Grain 3G, 5Gcooler, 5Gpot, platechiller')
    bx = recipeReader.bsmxStages(badTunDeadSpaceBsmx(),
                                 ctrl.setupControllers(False, True, True, myequipment))
    print(bx.getTunDeadSpace())
    print(bx.getRecipeName())
    print(bx.isValid())
    assert not bx.isValid()
    print(str(bx.getStages()))
    print(myname(), "OK")


def test_getVolQt():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    v = bx.getVolQt('F_E_MASH_VOL')
    assert isinstance(v, float)
    assert abs(v - 20.0) < 0.1
    print(myname(), "OK")


def test_getWeightLb():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    w = bx.getWeightLb('F_MH_GRAIN_WEIGHT')
    assert isinstance(w, float)
    assert abs(w - 7.25) < 0.1
    print(myname(), "OK")


def test_getTempF():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    t = bx.getTempF('F_MH_GRAIN_TEMP')
    assert isinstance(t, float)
    assert abs(t - 68.0) < 0.1
    print(myname(), "OK")


def myname():
    return(inspect.stack()[1][3])


def test_getTimeMin():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    t = bx.getTimeMin('F_MS_STEP_TIME')
    assert isinstance(t, float)
    assert abs(t - 60.0) < 0.1
    print(myname(), "OK")


def test_getMashProfile():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    mp = bx.getMashProfile()
    assert isinstance(mp, str) or isinstance(mp, unicode)
    assert mp == 'Single Infusion, Medium Body, No Mash Out'
    print(myname(), "OK")


def test_getEquipment():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    e = bx.getEquipment()
    assert isinstance(e, str) or isinstance(e, unicode)
    assert e == 'Grain 2.5G, 5Gcooler, 4Gpot'
    print(myname(), "OK")


def test_getGrainAbsorption():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    g = bx.getGrainAbsorption()
    assert isinstance(g, float)
    assert abs(g - 3.49) < 0.01
    print(myname(), "OK")


def test_getTunDeadSpace():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getTunDeadSpace()
    assert isinstance(ds, float)
    assert abs(ds - 0.2) < 0.01
    print(myname(), "OK")


def test_getStrikeVolume():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getStrikeVolume()
    assert isinstance(ds, float)
    assert abs(ds - 9.2625) < 0.01
    print(myname(), "OK")


def test_getPreBoilVolume():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getPreBoilVolume()
    assert isinstance(ds, float)
    assert abs(ds - 13.648) < 0.01
    print(myname(), "OK")


def test_getSpargeVolume():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    ds = bx.getSpargeVolume()
    assert isinstance(ds, float)
    assert abs(ds - 8.07947590361) < 0.01
    print(myname(), "OK")


def test_getDispense():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    d = bx.getDispense()
    assert isinstance(d, list)
    assert d == [60.0, 15.0]
    print(myname(), "OK")


def test_getDispenserAtTime():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    d1 = bx.getDispenserAtTime(60)
    assert isinstance(d1, str)
    assert d1 == 'dispenser1'

    d2 = bx.getDispenserAtTime(15.1)
    assert isinstance(d2, str)
    assert d2 == 'dispenser2'

    d3 = bx.getDispenserAtTime(0.0)
    assert isinstance(d3, str)
    assert d3 == 'error'

    print(myname(), "OK")


def test_getMisc():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    m = bx.getMisc()
    assert isinstance(m, list)
    assert m == [15.0]
    print(myname(), "OK")


def test_getHops():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    h = bx.getHops()
    assert isinstance(h, list)
    assert h == [60]
    print(myname(), "OK")


def test_prettyPrintStages():
    bx = recipeReader.bsmxStages(elaborateBsmx(), ctrlBsmxList())
    bx.prettyPrintStages()
    print(myname(), "OK")


def test_isValid():
    bx = recipeReader.bsmxStages(simpleBsmx(), ctrlBsmxList())
    assert bx.getRecipeName() == "18 Rune Stone  IPA 2.5G"
    assert not bx.isValid()
    print(os.getcwd())
    e = equipment.allEquipment('src/equipment/*.yaml')
    myequipment = e.get('Grain 2.5G, 5Gcooler, 4Gpot')
    cx = recipeReader.bsmxStages(elaborateBsmx(),
                                 ctrl.setupControllers(False, True, True, myequipment))
    assert not cx.isValid()
    cp = os.path.dirname(__file__)
    print(cp)
    rp = cp + "/../../beersmith/18RuneStoneIPA.bsmx"
    print(rp)
    dx = recipeReader.bsmxStages(rp, ctrl.setupControllers(False, True, True, myequipment))
    assert dx.isValid()
    print(myname(), "OK")


if __name__ == "__main__":
    test_badTunDeadSpace()
    test_GoodRecipe()
    #sys.exit()
    test_badProfile()
    test_testbatchsparge()
    test_testcold()
    test_isValid()
    test_init_bsmxStages_string()
    test_init_bsmxStages_file()
    test_init_bsmxStages_doc()
    test_getFieldStr()
    test_getVolG()
    test_getVolQt()
    test_getWeightLb()
    test_getTempF()
    test_getTimeMin()
    test_getMashProfile()
    test_getEquipment()
    test_getGrainAbsorption()
    test_getTunDeadSpace()
    test_getStrikeVolume()
    test_getPreBoilVolume()
    test_getSpargeVolume()
    test_getDispense()
    test_getDispenserAtTime()
    test_getMisc()
    test_getHops()
    test_prettyPrintStages()
    print("=====SUCCESS=====")
