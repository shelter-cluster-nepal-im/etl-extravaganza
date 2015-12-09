package util;

import bean.*;
import java.sql.*;
import java.util.*;
import java.util.logging.*;

/**
 *
 * @author Gaurab Pradhan
 */
public class Trainings {

    public static List<TrainingBean> getTrainData(Connection con, String agencyName) {
        List<TrainingBean> mList = new ArrayList<TrainingBean>();
        PreparedStatement pstmt = null;
        try {
            String query = "SELECT *  FROM " + PropertiesUtil.getDbTable1() + " WHERE " + PropertiesUtil.getSplitBy() + " = ?";
            pstmt = con.prepareStatement(query);
            pstmt.setString(1, agencyName);
            ResultSet rs = pstmt.executeQuery();
            while (rs.next()) {
                TrainingBean bean = new TrainingBean();
//                //Who
                bean.setImplementingAgency(rs.getString(8));
                bean.setSourcingAgency(rs.getString(9));
                bean.setLocalPartnerAgency(rs.getString(10));
                bean.setContactName(rs.getString(11));
                bean.setContactEmail(rs.getString(12));
                bean.setContactPhoneNumber(rs.getString(13));
//                
//               //Where
                bean.setDistrict(rs.getString(14));
                bean.setVDCMunicipalities(rs.getString(15));
                bean.setMunicipalWard(rs.getString(16));
//
//                //What
                bean.setTrainingSub(rs.getString(17));
                bean.setAudience(rs.getString(18));
                bean.setTrainingTitle(rs.getString(19));
                bean.setDemonstrationConstructionIncluded(rs.getString(20));
                bean.setIECMaterialsDistributed(rs.getString(21));
                bean.setDurationofeachsession(rs.getString(22));//in hours	
                bean.setAmountPaidtoParticipants(rs.getString(23)); //NRP per participants	
                bean.setTotalCostPerTraining(rs.getString(24));
                bean.setTotalParticipants(rs.getString(25));
                bean.setMales(rs.getString(26));
                bean.setFemales(rs.getString(27));
                bean.setThirdGender(rs.getString(28));
                bean.setElderly(rs.getString(29));//60+
                bean.setChildren(rs.getString(30));//u18	
                bean.setPersonswithDisabilities(rs.getString(31));
                bean.setVulnerableCasteorEthnicity(rs.getString(32));
                bean.setFemaleHH(rs.getString(33));
//                //When
                bean.setActivityStatus(rs.getString(34));
                bean.setDDStart(rs.getString(36));
                bean.setMMStart(rs.getString(37));
                bean.setYYStart(rs.getString(38));
                bean.setDDComp(rs.getString(40));
                bean.setMMComp(rs.getString(41));
                bean.setYYComp(rs.getString(42));

                bean.setAdditionalComments(rs.getString(43));
                mList.add(bean);
            }
            rs.close();
        } catch (SQLException ex) {
            Logger.getLogger(Distributions.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            if (pstmt != null) {
                try {
                    pstmt.close();
                } catch (SQLException ex) {
                    Logger.getLogger(Trainings.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
        return mList;
    }
}
