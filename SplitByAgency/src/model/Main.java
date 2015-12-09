package model;

import bean.*;
import java.io.*;
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
import org.apache.poi.ss.usermodel.*;
import util.*;

/**
 *
 * @author Gaurab Pradhan
 */
public class Main {

    public static void main(String[] args) throws IOException, FileNotFoundException, InvalidFormatException {
        Connection con = null;
        try {
            PropertiesUtil.loadPropertiesFile();
            con = DBConnection.getConnection();
            List<AgencyNameBean> agenciesName = new ArrayList<AgencyNameBean>();
            agenciesName = getImpAgenciesName(con);
            for (int i = 0; i < agenciesName.size(); i++) {
                String fname = "temp";
                List<DistBean> distList = Distributions.getDistData(con, agenciesName.get(i).toString());
                List<TrainingBean> trainList = Trainings.getTrainData(con, agenciesName.get(i).toString());
                System.out.println("Processing : " + agenciesName.get(i).toString());
                fname = agenciesName.get(i).toString().replaceAll("/", "-");
                if (distList.size() > 0) {
                    if (trainList.isEmpty()) {
                        writeToExcle(distList, fname);
                    } else {
                        writeToExcle(distList, trainList, fname);
                    }
                } else {
                    System.out.println("Distribution Sheet is Empty.");
                }
                distList = null;
                trainList = null;
            }
            agenciesName = null;
            // for generating HDX DB
            HDX.getDataForHDX(con, "db-HDX");
        } catch (Exception ex) {
            Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            try {
                if (con != null) {
                    con.close();
                }
            } catch (SQLException e) {
                Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, e);
            }
        } 
    }

    private static List<AgencyNameBean> getImpAgenciesName(Connection con) throws SQLException {
        List<AgencyNameBean> agenciesName = new ArrayList<AgencyNameBean>();
        Statement stmt = null;
        if (con != null) {
            System.out.println("Database Connection Established");
            stmt = con.createStatement();
//            String query = "SELECT DISTINCT imp_agency FROM " + PropertiesUtil.getDbTable();
            String query = "SELECT DISTINCT " + PropertiesUtil.getSplitBy() + " FROM " + PropertiesUtil.getDbTable();
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                AgencyNameBean bean = new AgencyNameBean();
                bean.setImp_agency(rs.getString(PropertiesUtil.getSplitBy()));
                agenciesName.add(bean);
            }
            rs.close();

        } else {
            System.out.println("Failed to make connection!");
        }
        return agenciesName;
    }

    private static void writeToExcle(List<DistBean> mainList, String fname) throws FileNotFoundException, IOException, InvalidFormatException {
        InputStream file = new FileInputStream(PropertiesUtil.getTemplateFile());
        Workbook workbook = WorkbookFactory.create(file);
        org.apache.poi.ss.usermodel.Sheet sheet = workbook.getSheetAt(1);
        int rowIndex = 1;
        for (DistBean bean : mainList) {
            Row row = sheet.createRow(rowIndex);
            //who
            row.createCell(0).setCellValue(bean.getImplementingAgency());
            row.createCell(1).setCellValue(bean.getSourcingAgency());
            row.createCell(2).setCellValue(bean.getLocalPartnerAgency());
            row.createCell(3).setCellValue(bean.getContactName());
            row.createCell(4).setCellValue(bean.getContactEmail());
            row.createCell(5).setCellValue(bean.getContactPhoneNumber());
            //where
            row.createCell(6).setCellValue(bean.getDistrict());
            row.createCell(7).setCellValue(bean.getVDCMunicipalities());
            row.createCell(8).setCellValue(bean.getMunicipalWard());
            //What
            row.createCell(9).setCellValue(bean.getActionType());
            row.createCell(10).setCellValue(bean.getActionDescription());
            row.createCell(11).setCellValue(bean.getTargeting());
            row.createCell(12).setCellValue(bean.getItems());
            row.createCell(13).setCellValue(bean.getTotalNumberHouseholds());
            row.createCell(14).setCellValue(bean.getAverageCostPerHouseholds());
            row.createCell(15).setCellValue(bean.getFemaleHeadedHouseholds());
            row.createCell(16).setCellValue(bean.getVulnerableCasteEthnicityHouseholds());
//                    //When
            row.createCell(17).setCellValue(bean.getActivityStatus());
            row.createCell(18).setCellValue(bean.getDDStart());
            row.createCell(19).setCellValue(bean.getMMStart());
            row.createCell(20).setCellValue(bean.getYYStart());
            row.createCell(21).setCellValue(bean.getDDComp());
            row.createCell(22).setCellValue(bean.getMMComp());
            row.createCell(23).setCellValue(bean.getYYComp());
//            row.createCell(18).setCellValue(bean.getStartDate());
//            row.createCell(19).setCellValue(bean.getCompletionDate());
            row.createCell(24).setCellValue(bean.getAdditionalComments());
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

    private static void writeToExcle(List<DistBean> distList, List<TrainingBean> trainList, String fname) throws FileNotFoundException, IOException, InvalidFormatException {
        InputStream file = new FileInputStream(PropertiesUtil.getTemplateFile());
        Workbook workbook = WorkbookFactory.create(file);
        org.apache.poi.ss.usermodel.Sheet sheet = workbook.getSheetAt(1);
        int rowIndex = 1;
        for (DistBean bean : distList) {
            Row row = sheet.createRow(rowIndex);
            //who
            row.createCell(0).setCellValue(bean.getImplementingAgency());
            row.createCell(1).setCellValue(bean.getSourcingAgency());
            row.createCell(2).setCellValue(bean.getLocalPartnerAgency());
            row.createCell(3).setCellValue(bean.getContactName());
            row.createCell(4).setCellValue(bean.getContactEmail());
            row.createCell(5).setCellValue(bean.getContactPhoneNumber());
            //where
            row.createCell(6).setCellValue(bean.getDistrict());
            row.createCell(7).setCellValue(bean.getVDCMunicipalities());
            row.createCell(8).setCellValue(bean.getMunicipalWard());
            //What
            row.createCell(9).setCellValue(bean.getActionType());
            row.createCell(10).setCellValue(bean.getActionDescription());
            row.createCell(11).setCellValue(bean.getTargeting());
            row.createCell(12).setCellValue(bean.getItems());
            row.createCell(13).setCellValue(bean.getTotalNumberHouseholds());
            row.createCell(14).setCellValue(bean.getAverageCostPerHouseholds());
            row.createCell(15).setCellValue(bean.getFemaleHeadedHouseholds());
            row.createCell(16).setCellValue(bean.getVulnerableCasteEthnicityHouseholds());
//                    //When
            row.createCell(17).setCellValue(bean.getActivityStatus());
//            row.createCell(18).setCellValue(bean.getStartDate());
//            row.createCell(19).setCellValue(bean.getCompletionDate());
//            row.createCell(20).setCellValue(bean.getAdditionalComments());
            row.createCell(18).setCellValue(bean.getDDStart());
            row.createCell(19).setCellValue(bean.getMMStart());
            row.createCell(20).setCellValue(bean.getYYStart());
            row.createCell(21).setCellValue(bean.getDDComp());
            row.createCell(22).setCellValue(bean.getMMComp());
            row.createCell(23).setCellValue(bean.getYYComp());
            row.createCell(24).setCellValue(bean.getAdditionalComments());
            rowIndex++;
        }
        //Trainings
        org.apache.poi.ss.usermodel.Sheet sheetT = workbook.getSheetAt(2);
        rowIndex = 1;
        for (TrainingBean bean : trainList) {
            Row row = sheetT.createRow(rowIndex);
////            //who
            row.createCell(0).setCellValue(bean.getImplementingAgency());
            row.createCell(1).setCellValue(bean.getSourcingAgency());
            row.createCell(2).setCellValue(bean.getLocalPartnerAgency());
            row.createCell(3).setCellValue(bean.getContactName());
            row.createCell(4).setCellValue(bean.getContactEmail());
            row.createCell(5).setCellValue(bean.getContactPhoneNumber());
////            //where
            row.createCell(6).setCellValue(bean.getDistrict());
            row.createCell(7).setCellValue(bean.getVDCMunicipalities());
            row.createCell(8).setCellValue(bean.getMunicipalWard());
////            //What
            row.createCell(9).setCellValue(bean.getTrainingSub());
            row.createCell(10).setCellValue(bean.getAudience());
            row.createCell(11).setCellValue(bean.getTrainingTitle());
            row.createCell(12).setCellValue(bean.getDemonstrationConstructionIncluded());
            row.createCell(13).setCellValue(bean.getIECMaterialsDistributed());
            row.createCell(14).setCellValue(bean.getDurationofeachsession());
            row.createCell(15).setCellValue(bean.getAmountPaidtoParticipants());
            row.createCell(16).setCellValue(bean.getTotalCostPerTraining());
            row.createCell(17).setCellValue(bean.getTotalParticipants());
            row.createCell(18).setCellValue(bean.getMales());
            row.createCell(19).setCellValue(bean.getFemales());
            row.createCell(20).setCellValue(bean.getThirdGender());
            row.createCell(21).setCellValue(bean.getElderly());
            row.createCell(22).setCellValue(bean.getChildren());
            row.createCell(23).setCellValue(bean.getPersonswithDisabilities());
            row.createCell(24).setCellValue(bean.getVulnerableCasteorEthnicity());
            row.createCell(25).setCellValue(bean.getFemaleHH());
////                    //When
            row.createCell(26).setCellValue(bean.getActivityStatus());
            row.createCell(27).setCellValue(bean.getDDStart());
            row.createCell(28).setCellValue(bean.getMMStart());
            row.createCell(29).setCellValue(bean.getYYStart());
            row.createCell(30).setCellValue(bean.getDDComp());
            row.createCell(31).setCellValue(bean.getMMComp());
            row.createCell(32).setCellValue(bean.getYYComp());
            row.createCell(33).setCellValue(bean.getAdditionalComments());
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
