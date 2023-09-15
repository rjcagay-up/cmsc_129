import java.awt.*; 
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;


public class PE01 {
   
    public static void mainWindow(){
    
     //Custom colors used for the UI/UX
     Color darkClr = new Color(36,39,40);
     Color aplClr = new Color(58,75,66);
     //Color whtClr = new Color(99,99,100);
        
     //Panels and defining component designs
        //Top
            //Add buttons
            JButton btn1 = new JButton("Load File");
            btn1.setBounds(125, 30, 170, 40); // Set position and size
            btn1.setFont(new Font("Arial", Font.BOLD, 16)); // Customize font
            btn1.setForeground(Color.white); // Set text color
            btn1.setBackground(aplClr); // Set background color 

            JButton btn2 =  new JButton("Process");
            btn2.setBounds(100, 30, 150, 40); // Set position and size
            btn2.setFont(new Font("Arial", Font.BOLD, 16)); // Customize font
            btn2.setForeground(Color.WHITE); // Set text color
            btn2.setBackground(aplClr); // Set background color

            //Top Panels
            JPanel topPanel1  = new JPanel();
            topPanel1.setBackground(darkClr);
            topPanel1.setBounds(0, 0, 375, 100);
            topPanel1.setLayout(null);

            JPanel topPanel2  = new JPanel();
            topPanel2.setBackground(darkClr);
            topPanel2.setBounds(375, 0, 375, 100);
            topPanel2.setLayout(null);



        //Middle
            //Labels
            JLabel label1 = new JLabel("Transition Table");
            label1.setForeground(Color.white);


            JLabel label2 = new JLabel("Input");
            label2.setForeground(Color.white);

            JLabel label3 = new JLabel("Output");
            label3.setForeground(Color.white);


            //Table
            // JTable table = new JTable();
                Object[][] data = {
                    {"John", "Doe", 30},
                    {"Jane", "Smith", 25},
                    // Add more rows as needed
                };
                String[] columnNames = {"First Name", "Last Name", "Age"};
                JTable table = new JTable(data, columnNames);
                JScrollPane scrollPane = new JScrollPane(table);
            
            //Panels
            JPanel midPanel1  = new JPanel();
            midPanel1.setBackground(darkClr);
            midPanel1.setBounds(0, 100, 250, 300);

            JPanel midPanel2  = new JPanel();
            midPanel2.setBackground(darkClr);
            midPanel2.setBounds(250, 100, 250, 300);

            JPanel midPanel3  = new JPanel();
            midPanel3.setBackground(darkClr);
            midPanel3.setBounds(500, 100, 250, 300);
        
        //Bottom Panel
            JPanel BtmPanel = new JPanel();
            BtmPanel.setBackground(Color.yellow);
            BtmPanel.setBounds(0,400,750,100);
        
        //Define and create main frame
            JFrame frame= new JFrame("CMSC 129");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setLayout(null);
            frame.setSize(750, 550);
            frame.setVisible(true);

        //Add components
         //Top
            //Column 1
            topPanel1.add(btn1, BorderLayout.CENTER);
            frame.add(topPanel1);

            //Column 2
            topPanel2.add(btn2, BorderLayout.CENTER);
            frame.add(topPanel2);

         //Middle
            //Column 1
            midPanel1.add(label1);
            midPanel1.add(table);
            frame.add(scrollPane, BorderLayout.CENTER);
            frame.add(midPanel1);

            //Column 2
            midPanel2.add(label2);
            frame.add(midPanel2);

            //Column 3
            midPanel3.add(label3);
            frame.add(midPanel3);

         //Bottom

            frame.add(BtmPanel);
    }
   

    public static void main(String[] args) {
        System.out.println("Jeren");
        mainWindow();
     }
}
