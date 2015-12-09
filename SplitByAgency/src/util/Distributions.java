package util;

import bean.*;
import java.sql.*;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Gaurab Pradhan
 */
public class Distributions {

    public static List<DistBean> getDistData(Connection con, String agencyName) {
        List<DistBean> mList = new ArrayList<DistBean>();
        PreparedStatement pstmt = null;
        try {
            String query = "SELECT *  FROM " + PropertiesUtil.getDbTable() + " WHERE " + PropertiesUtil.getSplitBy() + " = ?";
            pstmt = con.prepareStatement(query);
            pstmt.setString(1, agencyName);
            ResultSet rs = pstmt.executeQuery();
            while (rs.next()) {
                DistBean bean = new DistBean();
                //Who
                bean.setImplementingAgency(rs.getString(8));
                bean.setSourcingAgency(rs.getString(9));
                bean.setLocalPartnerAgency(rs.getString(10));
                bean.setContactName(rs.getString(11));
                bean.setContactEmail(rs.getString(12));
                bean.setContactPhoneNumber(rs.getString(13));
//
//                    //Where
                bean.setDistrict(rs.getString(14));
                bean.setVDCMunicipalities(rs.getString(15));
                bean.setMunicipalWard(rs.getString(16));
//
//                    //What
                bean.setActionType(rs.getString(17));
                bean.setActionDescription(rs.getString(18));
                bean.setTargeting(rs.getString(19));
                bean.setItems(rs.getString(20));
                bean.setTotalNumberHouseholds(rs.getString(21));
                bean.setAverageCostPerHouseholds(rs.getString(22));
                bean.setFemaleHeadedHouseholds(rs.getString(23));
                bean.setVulnerableCasteEthnicityHouseholds(rs.getString(24));

//                    //When
                bean.setActivityStatus(rs.getString(25));
                bean.setDDStart(rs.getString(27));
                bean.setMMStart(rs.getString(28));
                bean.setYYStart(rs.getString(29));
                bean.setDDComp(rs.getString(31));
                bean.setMMComp(rs.getString(32));
                bean.setYYComp(rs.getString(33));
//
                bean.setAdditionalComments(rs.getString(34));
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
