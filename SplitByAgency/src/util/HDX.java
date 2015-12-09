package util;

import bean.DistBean;
import bean.TrainingBean;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.*;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;

/**
 *
 * @author Gaurab Pradhan
 */
public class HDX {

    public static void getDataForHDX(Connection con, String filename) throws Exception {
        List<DistBean> distList = getDistData(con);
        List<TrainingBean> trainList = getTrainData(con);
        System.out.println("Processing to generate HDX DB");
        if (distList.size() > 0) {
            writeToHDXExcle(distList, trainList, filename);
        } else {
            System.out.println("Distribution Sheet is Empty.");
        }
        distList = null;
        trainList = null;
    }

    public static List<DistBean> getDistData(Connection con) {
        List<DistBean> mList = new ArrayList<DistBean>();
        Statement stmt = null;
        try {
            String query = "SELECT *  FROM " + PropertiesUtil.getDbTable();
            stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                DistBean bean = new DistBean();
                //first
                bean.setPriority(rs.getString(1));
                bean.setAccessMethods(rs.getString(2));
                bean.setHub(rs.getString(3));
                bean.setLastUpdate(rs.getString(4));
                bean.setDistrictHLCITCode(rs.getString(5));
                bean.setVDCHLCITCode(rs.getString(6));
//                bean.setPriority(rs.getString(7));
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
            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException ex) {
                    Logger.getLogger(HDX.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
        return mList;
    }

    public static List<TrainingBean> getTrainData(Connection con) {
        List<TrainingBean> mList = new ArrayList<TrainingBean>();
        Statement stmt = null;
        try {
            String query = "SELECT *  FROM " + PropertiesUtil.getDbTable1();
            stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                TrainingBean bean = new TrainingBean();
                //first
                bean.setPriority(rs.getString(1));
                bean.setAccessMethods(rs.getString(2));
                bean.setHub(rs.getString(3));
                bean.setLastUpdate(rs.getString(4));
                bean.setDistrictHLCITCode(rs.getString(5));
                bean.setVDCHLCITCode(rs.getString(6));
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
            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException ex) {
                    Logger.getLogger(HDX.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
        return mList;
    }

    public static void writeToHDXExcle(List<DistBean> distList, List<TrainingBean> trainList, String fname) throws FileNotFoundException, IOException, InvalidFormatException {
        InputStream file = new FileInputStream("DatabaseV5.0_09_11_2015for HDX.xlsx");
        Workbook workbook = WorkbookFactory.create(file);
        org.apache.poi.ss.usermodel.Sheet sheet = workbook.getSheetAt(0);
        int rowIndex = 1;
        for (DistBean bean : distList) {
            Row row = sheet.createRow(rowIndex);
            row.createCell(0).setCellValue(bean.getPriority());
            row.createCell(1).setCellValue(bean.getAccessMethods());
            row.createCell(2).setCellValue(bean.getHub());
            row.createCell(3).setCellValue(bean.getLastUpdate());
            row.createCell(4).setCellValue(bean.getDistrictHLCITCode());
            row.createCell(5).setCellValue(bean.getVDCHLCITCode());
            //who
            row.createCell(6).setCellValue(bean.getImplementingAgency());
            row.createCell(7).setCellValue(bean.getSourcingAgency());
            row.createCell(8).setCellValue(bean.getLocalPartnerAgency());
//            row.createCell(3).setCellValue(bean.getContactName());
//            row.createCell(4).setCellValue(bean.getContactEmail());
//            row.createCell(5).setCellValue(bean.getContactPhoneNumber());
            //where
            row.createCell(9).setCellValue(bean.getDistrict());
            row.createCell(10).setCellValue(bean.getVDCMunicipalities());
            row.createCell(11).setCellValue(bean.getMunicipalWard());
            //What
            row.createCell(12).setCellValue(bean.getActionType());
            row.createCell(13).setCellValue(bean.getActionDescription());
            row.createCell(14).setCellValue(bean.getTargeting());
            row.createCell(15).setCellValue(bean.getItems());
            row.createCell(16).setCellValue(bean.getTotalNumberHouseholds());
            row.createCell(17).setCellValue(bean.getAverageCostPerHouseholds());
            row.createCell(18).setCellValue(bean.getFemaleHeadedHouseholds());
            row.createCell(19).setCellValue(bean.getVulnerableCasteEthnicityHouseholds());
//                    //When
            row.createCell(20).setCellValue(bean.getActivityStatus());
//            row.createCell(18).setCellValue(bean.getStartDate());
//            row.createCell(19).setCellValue(bean.getCompletionDate());
//            row.createCell(20).setCellValue(bean.getAdditionalComments());
            row.createCell(21).setCellValue(bean.getDDStart() + "/" + bean.getMMStart() + "/" + bean.getYYStart());
            row.createCell(22).setCellValue(bean.getDDComp() + "/" + bean.getMMComp() + "/" + bean.getYYComp());
            row.createCell(23).setCellValue(bean.getAdditionalComments());
            rowIndex++;
        }
        //Trainings
        org.apache.poi.ss.usermodel.Sheet sheetT = workbook.getSheetAt(1);
        rowIndex = 1;
        for (TrainingBean bean : trainList) {
            Row row = sheetT.createRow(rowIndex);
            row.createCell(0).setCellValue(bean.getPriority());
            row.createCell(1).setCellValue(bean.getAccessMethods());
            row.createCell(2).setCellValue(bean.getHub());
            row.createCell(3).setCellValue(bean.getLastUpdate());
            row.createCell(4).setCellValue(bean.getDistrictHLCITCode());
            row.createCell(5).setCellValue(bean.getVDCHLCITCode());
////            //who
            row.createCell(6).setCellValue(bean.getImplementingAgency());
            row.createCell(7).setCellValue(bean.getSourcingAgency());
            row.createCell(8).setCellValue(bean.getLocalPartnerAgency());
//            row.createCell(3).setCellValue(bean.getContactName());
//            row.createCell(4).setCellValue(bean.getContactEmail());
//            row.createCell(5).setCellValue(bean.getContactPhoneNumber());
////            //where
            row.createCell(9).setCellValue(bean.getDistrict());
            row.createCell(10).setCellValue(bean.getVDCMunicipalities());
            row.createCell(11).setCellValue(bean.getMunicipalWard());
////            //What
            row.createCell(12).setCellValue(bean.getTrainingSub());
            row.createCell(13).setCellValue(bean.getAudience());
            row.createCell(14).setCellValue(bean.getTrainingTitle());
            row.createCell(15).setCellValue(bean.getDemonstrationConstructionIncluded());
            row.createCell(16).setCellValue(bean.getIECMaterialsDistributed());
            row.createCell(17).setCellValue(bean.getDurationofeachsession());
            row.createCell(18).setCellValue(bean.getAmountPaidtoParticipants());
            row.createCell(19).setCellValue(bean.getTotalCostPerTraining());
            row.createCell(20).setCellValue(bean.getTotalParticipants());
            row.createCell(21).setCellValue(bean.getMales());
            row.createCell(22).setCellValue(bean.getFemales());
            row.createCell(23).setCellValue(bean.getThirdGender());
            row.createCell(24).setCellValue(bean.getElderly());
            row.createCell(25).setCellValue(bean.getChildren());
            row.createCell(26).setCellValue(bean.getPersonswithDisabilities());
            row.createCell(27).setCellValue(bean.getVulnerableCasteorEthnicity());
            row.createCell(28).setCellValue(bean.getFemaleHH());
////                    //When
            row.createCell(29).setCellValue(bean.getActivityStatus());
            row.createCell(30).setCellValue(bean.getDDStart() + "/" + bean.getMMStart() + "/" + bean.getYYStart());
            row.createCell(31).setCellValue(bean.getDDComp() + "/" + bean.getMMComp() + "/" + bean.getYYComp());
            row.createCell(32).setCellValue(bean.getAdditionalComments());
            rowIndex++;
        }

        //Writing into excel file
        DateFormat dateFormat = new SimpleDateFormat("ddMMyyyy");
        Calendar cal = Calendar.getInstance();
        String todayDate = dateFormat.format(cal.getTime());

        String filePath = PropertiesUtil.getFilePath();
        File folder = new File(filePath);
        if (!folder.exists()) {
            if (folder.mkdir()) {
                System.out.println("Directory is created!");
            } else {
                System.out.println("Failed to create directory!");
            }
        }
        FileOutputStream fos = new FileOutputStream(filePath + fname + " - " + todayDate + ".xlsx");
        workbook.write(fos);
        System.out.println(filePath + fname + " - " + todayDate + ".xlsx created");
        fos.close();
    }
}
