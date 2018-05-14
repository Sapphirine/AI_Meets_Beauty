import org.jsoup.Jsoup;
import org.jsoup.helper.Validate;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import com.opencsv.CSVReader;
import java.io.FileReader;
import java.io.IOException;
import com.opencsv.CSVWriter;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;


public class labeler {

    public static void main(String[] args) {

        String csvFile = "./links2K.csv";

        CSVReader reader = null;

        Writer writer = null;
        try {
            reader = new CSVReader(new FileReader(csvFile));
            writer = Files.newBufferedWriter(Paths.get("./links2KLabeled.csv"));

            CSVWriter csvWriter = new CSVWriter(writer,
                    CSVWriter.DEFAULT_SEPARATOR,
                    CSVWriter.DEFAULT_QUOTE_CHARACTER,
                    CSVWriter.DEFAULT_ESCAPE_CHARACTER,
                    CSVWriter.DEFAULT_LINE_END);
            String[] line;
            int counter = 0;
            while ((line = reader.readNext()) != null) {
                counter++;
                System.out.println("id = " + line[0] + "url= " + line[1]);
                String bestGuess = null;
                String newUrl = "http://www.google.com/searchbyimage?hl=en&image_url="+line[1];
                try {
                    Document doc = Jsoup.connect(newUrl).userAgent("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36").get();
                    Elements bestGuessElement = doc.select("a.fKDtNb");

                    if (!bestGuessElement.isEmpty() && bestGuessElement.hasText()) {
                        bestGuess = bestGuessElement.text();
                    }
                    //System.out.println(bestGuess);
                }catch(Exception e){
                    System.out.print(e.toString());
                }
                if(bestGuess!=null) {
                    String label = "";
                    for(int i = 1; i < line.length; i++){
                        label+=line[i];
                    }
                    csvWriter.writeNext(new String[]{line[0], label, bestGuess});
                }
                else
                    csvWriter.writeNext(new String[]{line[0], line[1], "Not Supported"});

            }
            System.out.println("Counter is: "+counter);


        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
