package bean;

import java.sql.Connection;
import java.util.List;

/**
 *
 * @author Gaurab Pradhan
 */
public class TrainingBean {
//first
    private String Priority;	
    private String AccessMethods;
    private String Hub;
    private String LastUpdate;
    private String DistrictHLCITCode;
    private String VDCHLCITCode;
//who
    private String ImplementingAgency;
    private String SourcingAgency;
    private String LocalPartnerAgency;
    private String ContactName;
    private String ContactEmail;
    private String ContactPhoneNumber;
//where
    private String District;
    private String VDCMunicipalities;
    private String MunicipalWard;
//What
    private String TrainingSub;
    private String Audience;
    private String TrainingTitle;
    private String DemonstrationConstructionIncluded;
    private String IECMaterialsDistributed;
    private String Durationofeachsession;//in hours	
    private String AmountPaidtoParticipants; //NRP per participants	
    private String TotalCostPerTraining;
    private String TotalParticipants;
    private String Males;
    private String Females;
    private String ThirdGender;
    private String Elderly;//60+
    private String Children;//u18	
    private String PersonswithDisabilities;
    private String VulnerableCasteorEthnicity;
    private String FemaleHH;
//when
    private String ActivityStatus;
    private String DDStart;
    private String MMStart;
    private String YYStart;
    private String DDComp;
    private String MMComp;
    private String YYComp;

    private String AdditionalComments;

    public String getPriority() {
        return Priority;
    }

    public void setPriority(String Priority) {
        this.Priority = Priority;
    }

    public String getAccessMethods() {
        return AccessMethods;
    }

    public void setAccessMethods(String AccessMethods) {
        this.AccessMethods = AccessMethods;
    }

    public String getHub() {
        return Hub;
    }

    public void setHub(String Hub) {
        this.Hub = Hub;
    }

    public String getLastUpdate() {
        return LastUpdate;
    }

    public void setLastUpdate(String LastUpdate) {
        this.LastUpdate = LastUpdate;
    }

    public String getDistrictHLCITCode() {
        return DistrictHLCITCode;
    }

    public void setDistrictHLCITCode(String DistrictHLCITCode) {
        this.DistrictHLCITCode = DistrictHLCITCode;
    }

    public String getVDCHLCITCode() {
        return VDCHLCITCode;
    }

    public void setVDCHLCITCode(String VDCHLCITCode) {
        this.VDCHLCITCode = VDCHLCITCode;
    }

    
    public String getImplementingAgency() {
        return ImplementingAgency;
    }

    public void setImplementingAgency(String ImplementingAgency) {
        this.ImplementingAgency = ImplementingAgency;
    }

    public String getSourcingAgency() {
        return SourcingAgency;
    }

    public void setSourcingAgency(String SourcingAgency) {
        this.SourcingAgency = SourcingAgency;
    }

    public String getLocalPartnerAgency() {
        return LocalPartnerAgency;
    }

    public void setLocalPartnerAgency(String LocalPartnerAgency) {
        this.LocalPartnerAgency = LocalPartnerAgency;
    }

    public String getContactName() {
        return ContactName;
    }

    public void setContactName(String ContactName) {
        this.ContactName = ContactName;
    }

    public String getContactEmail() {
        return ContactEmail;
    }

    public void setContactEmail(String ContactEmail) {
        this.ContactEmail = ContactEmail;
    }

    public String getContactPhoneNumber() {
        return ContactPhoneNumber;
    }

    public void setContactPhoneNumber(String ContactPhoneNumber) {
        this.ContactPhoneNumber = ContactPhoneNumber;
    }

    public String getDistrict() {
        return District;
    }

    public void setDistrict(String District) {
        this.District = District;
    }

    public String getVDCMunicipalities() {
        return VDCMunicipalities;
    }

    public void setVDCMunicipalities(String VDCMunicipalities) {
        this.VDCMunicipalities = VDCMunicipalities;
    }

    public String getMunicipalWard() {
        return MunicipalWard;
    }

    public void setMunicipalWard(String MunicipalWard) {
        this.MunicipalWard = MunicipalWard;
    }

    public String getTrainingSub() {
        return TrainingSub;
    }

    public void setTrainingSub(String TrainingSub) {
        this.TrainingSub = TrainingSub;
    }

    public String getAudience() {
        return Audience;
    }

    public void setAudience(String Audience) {
        this.Audience = Audience;
    }

    public String getTrainingTitle() {
        return TrainingTitle;
    }

    public void setTrainingTitle(String TrainingTitle) {
        this.TrainingTitle = TrainingTitle;
    }

    public String getDemonstrationConstructionIncluded() {
        return DemonstrationConstructionIncluded;
    }

    public void setDemonstrationConstructionIncluded(String DemonstrationConstructionIncluded) {
        this.DemonstrationConstructionIncluded = DemonstrationConstructionIncluded;
    }

    public String getIECMaterialsDistributed() {
        return IECMaterialsDistributed;
    }

    public void setIECMaterialsDistributed(String IECMaterialsDistributed) {
        this.IECMaterialsDistributed = IECMaterialsDistributed;
    }

    public String getDurationofeachsession() {
        return Durationofeachsession;
    }

    public void setDurationofeachsession(String Durationofeachsession) {
        this.Durationofeachsession = Durationofeachsession;
    }

    public String getAmountPaidtoParticipants() {
        return AmountPaidtoParticipants;
    }

    public void setAmountPaidtoParticipants(String AmountPaidtoParticipants) {
        this.AmountPaidtoParticipants = AmountPaidtoParticipants;
    }

    public String getTotalCostPerTraining() {
        return TotalCostPerTraining;
    }

    public void setTotalCostPerTraining(String TotalCostPerTraining) {
        this.TotalCostPerTraining = TotalCostPerTraining;
    }

    public String getTotalParticipants() {
        return TotalParticipants;
    }

    public void setTotalParticipants(String TotalParticipants) {
        this.TotalParticipants = TotalParticipants;
    }

    public String getMales() {
        return Males;
    }

    public void setMales(String Males) {
        this.Males = Males;
    }

    public String getFemales() {
        return Females;
    }

    public void setFemales(String Females) {
        this.Females = Females;
    }

    public String getThirdGender() {
        return ThirdGender;
    }

    public void setThirdGender(String ThirdGender) {
        this.ThirdGender = ThirdGender;
    }

    public String getElderly() {
        return Elderly;
    }

    public void setElderly(String Elderly) {
        this.Elderly = Elderly;
    }

    public String getChildren() {
        return Children;
    }

    public void setChildren(String Children) {
        this.Children = Children;
    }

    public String getPersonswithDisabilities() {
        return PersonswithDisabilities;
    }

    public void setPersonswithDisabilities(String PersonswithDisabilities) {
        this.PersonswithDisabilities = PersonswithDisabilities;
    }

    public String getVulnerableCasteorEthnicity() {
        return VulnerableCasteorEthnicity;
    }

    public void setVulnerableCasteorEthnicity(String VulnerableCasteorEthnicity) {
        this.VulnerableCasteorEthnicity = VulnerableCasteorEthnicity;
    }

    public String getFemaleHH() {
        return FemaleHH;
    }

    public void setFemaleHH(String FemaleHH) {
        this.FemaleHH = FemaleHH;
    }

    public String getActivityStatus() {
        return ActivityStatus;
    }

    public void setActivityStatus(String ActivityStatus) {
        this.ActivityStatus = ActivityStatus;
    }

    public String getDDStart() {
        return DDStart;
    }

    public void setDDStart(String DDStart) {
        this.DDStart = DDStart;
    }

    public String getMMStart() {
        return MMStart;
    }

    public void setMMStart(String MMStart) {
        this.MMStart = MMStart;
    }

    public String getYYStart() {
        return YYStart;
    }

    public void setYYStart(String YYStart) {
        this.YYStart = YYStart;
    }

    public String getDDComp() {
        return DDComp;
    }

    public void setDDComp(String DDComp) {
        this.DDComp = DDComp;
    }

    public String getMMComp() {
        return MMComp;
    }

    public void setMMComp(String MMComp) {
        this.MMComp = MMComp;
    }

    public String getYYComp() {
        return YYComp;
    }

    public void setYYComp(String YYComp) {
        this.YYComp = YYComp;
    }

    
    public String getAdditionalComments() {
        return AdditionalComments;
    }

    public void setAdditionalComments(String AdditionalComments) {
        this.AdditionalComments = AdditionalComments;
    }
}
