import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;

public class FileLoaderGUI extends JFrame {
    private JTextArea inputTextArea;
    private JTable dfaTable;
    private DefaultTableModel tableModel;
    private JTextArea outputTextArea;
    //private StringBuilder content;
    //private JPanel mainPanel;
    private JPanel statusPanel;
    //private GridBagConstraints gbc;

    public FileLoaderGUI() {
        setTitle("CMSC 129 DFA Checker");
        setSize(800, 600); // Adjusted the initial size
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        //content = new StringBuilder();

     // Create a panel for the main content with GridBagLayout
        JPanel mainPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.BOTH; // Allow components to grow both horizontally and vertically
        gbc.weightx = 1.0; // Make components take up available horizontal space

    // Create a panel for the Status panel
       statusPanel = new JPanel();
       JLabel statusLabel = new JLabel("Status:");
       //Label UI
       statusPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
       statusPanel.add(statusLabel);

     // Create a panel for the Load and Process buttons
        // Load Button
        JPanel buttonPanel = new JPanel();
        JButton loadButton = new JButton("Load Files");
        loadButton.addActionListener(e -> loadFiles());
        buttonPanel.add(loadButton);

        // Process Button
        JButton processButton = new JButton("Process");
        processButton.addActionListener(e -> processFiles());
        buttonPanel.add(processButton);
       
        // Panel UI
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 3; // Span the buttons across all columns
        mainPanel.add(buttonPanel, gbc); // Put buttons above the UI
        buttonPanel.setBackground(Color.pink); //Set color to the panel

     // Create a panel for the Input label and its placeholder
       JPanel inputPanel = new JPanel(new BorderLayout());
       JLabel inputLabel = new JLabel("Input:");

       // Panel UI
       inputPanel.add(inputLabel, BorderLayout.NORTH);
       inputTextArea = new JTextArea(10, 40);
       JScrollPane inputScrollPane = new JScrollPane(inputTextArea); // Scroll function for the pane
       inputPanel.add(inputScrollPane, BorderLayout.CENTER);
       inputPanel.setBackground(Color.pink);
       inputPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
       gbc.gridx = 1;
       gbc.gridy = 1;
       gbc.gridwidth = 1;
       gbc.weighty = 2.0; // Increase weighty value for more vertical space
       mainPanel.add(inputPanel, gbc); // Put Input panel on the left

     // Create a panel for the Transition table label and its placeholder
       JPanel dfaPanel = new JPanel(new BorderLayout());
       JLabel dfaLabel = new JLabel("Transition table:");

       // Panel UI
       dfaPanel.add(dfaLabel, BorderLayout.NORTH);
       tableModel = new DefaultTableModel();
       dfaTable = new JTable(tableModel);
       JScrollPane dfaScrollPane = new JScrollPane(dfaTable);
       dfaPanel.add(dfaScrollPane, BorderLayout.CENTER);
       dfaPanel.setBackground(Color.pink); // Set Panel color
       dfaPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
       gbc.gridx = 0;
       gbc.gridy = 1;
       gbc.weighty = 2.0; // Increase weighty value for more vertical space
       mainPanel.add(dfaPanel, gbc); // Put Transition table panel in the center

     // Create a panel for the Output label and its placeholder
       JPanel outputPanel = new JPanel(new BorderLayout());
       JLabel outputLabel = new JLabel("Output:");
       outputPanel.add(outputLabel, BorderLayout.NORTH);
       // Panel UI
       
       outputTextArea = new JTextArea(10, 40);
       JScrollPane outputScrollPane = new JScrollPane(outputTextArea);
       outputPanel.add(outputScrollPane, BorderLayout.CENTER);
       outputPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
       gbc.gridx = 2;
       gbc.gridy = 1;
       gbc.weighty = 2.0; // Increase weighty value for more vertical space
       mainPanel.add(outputPanel, gbc); // Put Output panel on the right

     

       //Panel UI
       gbc.gridx = 0;
       gbc.gridy = 2;
       gbc.gridwidth = 3;
       gbc.weighty = 1.0;
       statusPanel.setBackground(Color.yellow);
       mainPanel.add(statusPanel, gbc);

       // Add the main content to the frame
       add(mainPanel, BorderLayout.CENTER);
   }


    // Method for loading files
    private void loadFiles() {
        JFileChooser fileChooser = new JFileChooser(System.getProperty("user.dir")); // Create a file chooser dialog and set the initial directory to the current working directory
        int result = fileChooser.showOpenDialog(this); // Show the dialog and get the user's choice

        if (result == JFileChooser.APPROVE_OPTION) { // If the user chooses a file
            File file = fileChooser.getSelectedFile(); // Get the selected file
            String fileName = file.getName(); // Get the name of the file

                

            try {
                BufferedReader reader = new BufferedReader(new FileReader(file)); // Create a reader for the file
                StringBuilder content = new StringBuilder(); // Create a string builder to store file content
                String line;
                while ((line = reader.readLine()) != null) { // Read each line of the file
                    content.append(line).append("\n"); // Append the line to the content with a newline
                }
                reader.close(); // Close the file reader

                if (fileName.endsWith(".in")) { // If the file has a .in extension
                    inputTextArea.setText(content.toString()); // Set the text in the inputTextArea
                    status(true, ".in");
                } else if (fileName.endsWith(".dfa")) { // If the file has a .dfa extension
                    processDFAFile(content.toString()); // Process and display the .dfa file
                    status(true, ".dfa");
                } else {
                    JOptionPane.showMessageDialog(this, "Unsupported file format."); // Show an error message for unsupported file formats
                }
            } catch (IOException e) {
                e.printStackTrace(); // Print the exception stack trace
                JOptionPane.showMessageDialog(this, "Error loading the file."); // Show an error message for file loading
            }
        }

        
    }

    // Method for processing DFA files
    private void processDFAFile(String fileContent) {
        // Split the content into lines
        String[] lines = fileContent.split("\n");

        if (lines.length < 2) { // If there are less than 2 lines in the file
            JOptionPane.showMessageDialog(this, "Invalid DFA file format."); // Show an error message for invalid format
            return; // Return from the method
        }

        // Extract the symbols from the first line
        String[] symbols = lines[0].trim().split(",");
        int numSymbols = symbols.length;

        // Create the table model with headers
        String[] columnHeaders = new String[numSymbols + 1];
        columnHeaders[0] = "";
        for (int i = 0; i < numSymbols; i++) {
            columnHeaders[i + 1] = symbols[i];
        }

        // Initialize the table model with headers and empty data
        tableModel.setColumnIdentifiers(columnHeaders);
        tableModel.setRowCount(lines.length - 1);

        // Populate the table rows
        for (int row = 1; row < lines.length; row++) {
            String[] cells = lines[row].trim().split(",");
            for (int col = 0; col < numSymbols+2; col++) {
                // if (col == 0) {
                //     tableModel.setValueAt(cells[0], row - 1, col);
                // } else {
                //     tableModel.setValueAt(cells[col], row - 1, col);
                // }

                // System.out.print(cells[col] + " ");

                if (cells[col].equals("-") || cells[col].equals("+") || cells[col].equals("")) {
                    cells[col+1] = cells[col+1] + cells[col];
                } else {
                    tableModel.setValueAt(cells[col], row - 1, col-1);
                }

            }
        }
    }

    // Method for processing files (placeholder for actual processing logic)
    private void processFiles() {
        // Add your processing logic here
        // You can use inputTextArea.getText() and dfaTextArea.getText() to access the loaded content
        // and update outputTextArea with the result
        // For this example, let's just copy the input to output
        status(true,"output");
        outputTextArea.setText(inputTextArea.getText());
    }

    private void status(boolean isSuccess, String fileType) {
        statusPanel.removeAll();
        JLabel okLabel = new JLabel();
        okLabel.setName("okLabel");
    
        if (isSuccess) {
            if (fileType.equals(".in") || fileType.equals(".dfa")){
                okLabel.setText("Status: SUCCESS importing " + fileType);
            
            }
            else if (fileType.equals("output")){
                okLabel.setText("Status: Processing " + fileType);
            }
            okLabel.setForeground(Color.BLACK); // Set text color to green for success

        } else {
            okLabel.setText("Status: ERROR");
            okLabel.setForeground(Color.RED); // Set text color to red for error
        }

        // Debugging information
        System.out.println("Adding label to Panel");
    
        // Check if an "okLabel" component exists in the statusPanel
        Component[] components = statusPanel.getComponents();
        for (Component component : components) {
            if (component.getName() != null && component.getName().equals("okLabel")) {
                okLabel.setText("");
                statusPanel.remove(okLabel); // Remove the previous okLabel
                okLabel.setText("SUCCESS importing " + fileType);
               
                System.out.println("Removed");
            }
            
        }
        
        // Add the new okLabel
        statusPanel.add(okLabel);

        // Refresh the panel
        statusPanel.revalidate();
        statusPanel.repaint();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                FileLoaderGUI fileLoader = new FileLoaderGUI();
                fileLoader.setVisible(true);
            }
        });
    }
}
