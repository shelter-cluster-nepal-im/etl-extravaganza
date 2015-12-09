package bean;
/**
 *
 * @author Gaurab Pradhan
 */
public class AgencyNameBean {
    private String imp_agency = "";

    public String getImp_agency() {
        return imp_agency;
    }

    public void setImp_agency(String imp_agency) {
        this.imp_agency = imp_agency;
    }
    
    public String toString() {

        StringBuilder str = new StringBuilder();
        str.append(this.imp_agency);
        return str.toString();
    }
}