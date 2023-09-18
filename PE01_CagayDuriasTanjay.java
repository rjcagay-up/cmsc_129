import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;
import java.awt.*;
import java.io.*;

public class PE01_CagayDuriasTanjay extends JFrame {
    private JTextArea inputTextArea;
    private JTable dfaTable;
    private DefaultTableModel tableModel;
    private JTextArea outputTextArea;
    private String outputFileName;
    private JPanel statusPanel;
  

    //Cutsom UI
    Font customFont = new Font("Arial", Font.BOLD, 20);
    Insets panelInsets = new Insets(10, 10, 10, 10);
    public PE01_CagayDuriasTanjay() {
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
       //UI
       statusPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
       statusPanel.add(statusLabel);
       statusLabel.setFont(customFont);

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

       //Label UI
       inputLabel.setFont(customFont);

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

       //Label UI
       dfaLabel.setFont(customFont);

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
        
       //Label UI
       outputLabel.setFont(customFont);

       // Panel UI
       outputTextArea = new JTextArea(10, 40);
       JScrollPane outputScrollPane = new JScrollPane(outputTextArea);
       outputTextArea.setFont(new Font("Arial", Font.PLAIN, 14));
       outputPanel.add(outputScrollPane, BorderLayout.CENTER);
       outputPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
       gbc.gridx = 2;
       gbc.gridy = 1;
       gbc.weighty = 2.0; // Increase weighty value for more vertical space
       mainPanel.add(outputPanel, gbc); // Put Output panel on the right
       outputPanel.setBackground(Color.pink); //Set color to the panel

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

                    String outputFileName = fileName.replace(".in", ".out");
                outputFileName = outputFileName.substring(0, outputFileName.lastIndexOf('.')) + ".out";

                // Store the modified output file name
                this.outputFileName = outputFileName;
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

        // Customize the font for the table headers
        JTableHeader header = dfaTable.getTableHeader();
        Font headerFont = new Font("Arial", Font.BOLD, 16); // Customize the font here
        header.setFont(headerFont);

        // Customize the font for the table cells
        Font cellFont = new Font("Arial", Font.ITALIC, 14); // Customize the font here
        dfaTable.setFont(cellFont);

         // Center-align the text in the cells
        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(JLabel.CENTER);
        dfaTable.setDefaultRenderer(Object.class, centerRenderer);

        // initializing counter for start state, state indicators, and additional to state names (for "-" and "+" indicators)
        int startStates = 0;
        String indicateStates = "";
        String stateName = "";

        // Populate the table rows
        for (int row = 1; row < lines.length; row++) {

            // Splits the DFA file format into individual states
            String[] cells = lines[row].trim().split(",");

            // Goes through each state and encodes into the table
            for (int col = 0; col < numSymbols+2; col++) {

                // due to splitting with "," character, "" are possible characters to encounter because of DFA format
                // when "-", "+" and "" (turned into " ") characters are stored in string indicateStates, separated by ","
                if (cells[col].equals("-")) {

                    startStates += 1; //if "-" character is detected, there is one start state present
                    indicateStates += "-,";

                } else if (cells[col].equals("+")) {

                    indicateStates += "+,";

                } else if (cells[col].equals("")) {

                    indicateStates += " ,";

                } else { // each column for each row is filled with the corresponding state, following the DFA file

                    // checks if current state name is valid
                    if (!(isvalidStateName(cells[col]))) {
                        tableModel.setRowCount(0); // erases invalid DFA table
                        JOptionPane.showMessageDialog(this, "Invalid DFA: Invalid State Name [only A-Z]"); // Show an error message for invalid DFA
                        return;
                    }

                    // if it is the first column of the row, add indicators if state is start, final, or not
                    if (col == 1) {
                        //indicateStates string is split by "," to individual indicators for each of the states in the first column (-,+,"")
                        String[] indicators = indicateStates.trim().split(",");
                        stateName = cells[col] + indicators[row - 1];
                    } else { // else, just display name
                        stateName = cells[col];
                    }

                    // sets value of the state name on the table
                    tableModel.setValueAt(stateName, row - 1, col - 1);
                
                }

            }
        }

        // if the number of start states is not one
        // given DFA is invalid
        if (startStates != 1) {
            tableModel.setRowCount(0); // erases invalid DFA table
            JOptionPane.showMessageDialog(this, "Invalid DFA: Only one start state must exist"); // Show an error message for invalid DFA
            return; // Return from the method
        }

    }
    
    // Checks if input string is a singular uppercase letter (A-Z)
    private boolean isvalidStateName (String str) {

        if (str.length() != 1) { // if length is not 1, it is not one letter
            return false;
        } else if (!(Character.isUpperCase(str.charAt(0)))) { // checks if it is uppercase
            return false;
        }
        // else
        return true;

    }

    // Method for processing files (placeholder for actual processing logic)
    private void processFiles() {
        
        // initializing variables
        int startState = 0;
        int currentState = 0;
        String nextState = "";

        // Get encoded text in Input Text Area
        String inputText = inputTextArea.getText();

        // Check if the input text is empty
        if (inputText.trim().isEmpty()) {
            JOptionPane.showMessageDialog(this, "No .in file found. Upload .in to process");
            return; // Exit the method if the input area is empty
        }

        // Check if the dfa table is empty
        if (tableModel.getRowCount() == 0 && tableModel.getColumnCount() == 0) {
            JOptionPane.showMessageDialog(this, "No .dfa file found. Upload .dfa to process");
            return; // Exit the method if the dfa table is empty
        }

        // Get possible inputs from DFA table headers
        String inputs = "";
        for (int col = 1; col < tableModel.getColumnCount(); col++) {
            inputs += (String) tableModel.getColumnName(col);
        }

        // Splits string inputs into possible character inputs from input strings
        String[] inputPossible = inputs.split("");

        startState = find_startState();

        // Splits the content into individual input strings
        String[] lines = inputText.split("\n");

        // Goes through each of the input strings
        for (int inputString = 0; inputString < lines.length; inputString++) {

            // begins with start state
            currentState = startState;

            // Uncomment line to track each input string
            // System.out.println("String: " + lines[inputString]);
            
            // Splits the input string into individual characters
            String[] inputStringCharacters = lines[inputString].split("");
            
            // Goes through each of the individual characters of the current input string
            for (int character = 0; character < inputStringCharacters.length; character++){

                // Uncomment line to track current state and read character
                // System.out.println("\nCurrent State: " + (String) tableModel.getValueAt(currentState, 0) + " Character Read: " + inputStringCharacters[character]);
                
                // Goes through each of the possible inputs and checks for matches
                for(int inputCheck = 0; inputCheck < inputs.length(); inputCheck++) {

                    // if it matches, it accesses the state on the column of the input and row of the current State
                    if (inputStringCharacters[character].equals(inputPossible[inputCheck])) {
                        
                        // the next state is designated, depending on the current state and the input character read in the string
                        // this refers again to the constructed DFA table
                        nextState = (String) tableModel.getValueAt(currentState, inputCheck+1);

                        // the current state is changed to the next state
                        currentState = findState(nextState);
                        
                    }

                }

            }
    
            // check if end state is final state, refering to the DFA
            if (if_FinalState(currentState)) {

                // if the end state is a final state, the input string is accepted by the machine and so is INVALID
                outputTextArea.append("VALID\n");
                
            } else {

                // if the end state is not a final state, the input string is not accepted by the machine and so is INVALID
                outputTextArea.append("INVALID\n");
                
            }

            // Uncomment to track when DFA tracking for input string is done
            // System.out.println("End...\n");

        }
      status(true,"output");
    
    
    // Display the output in the outputTextArea
     //outputTextArea.setText(outputTextArea.toString());
     
    
     outputTextArea.setText(outputTextArea.getText());

      // Create a StringBuilder to store the output
    StringBuilder outputStringBuilder = new StringBuilder();
    
    // Iterate through the output lines and append them to the StringBuilder
    String[] outputLines = outputTextArea.getText().split("\n");
    for (String outputLine : outputLines) {
        outputStringBuilder.append(outputLine).append("\n");
    }

    // Define the file path for saving the results using the modified output file name
    String outputPath = System.getProperty("user.dir") + File.separator + outputFileName;

    // Try to write the output to the file
    try (FileWriter writer = new FileWriter(outputPath)) {
        writer.write(outputStringBuilder.toString());
        writer.flush();
        writer.close();
        status(true, "output");

        // Display a message to inform the user that the results have been saved
        JOptionPane.showMessageDialog(this, "Results have been saved to " + outputFileName + "'.");
    } catch (IOException e) {
        e.printStackTrace(); // Handle the exception appropriately
        JOptionPane.showMessageDialog(this, "Error saving the results to" + outputFileName + "'.");
    }

    }

    // Method for finding start state in the constructed DFA table
    private int find_startState() {

        // initializing variables
        int startState = 0;

        // find the start state, number of rows in the table represents number of states
        for (int state = 0; state < tableModel.getRowCount(); state++) {

            // only start and final states have two characters in their table
            // this is to avoid going beyond index with the other states having only single characters
            // if the state only has one character, it is not the start state, continue
            if (((String) tableModel.getValueAt(state, 0)).length() == 2) {
                
                // retrieves object value of set row and column on the DFA table created and turn into string
                // string is then split per character
                String[] stateString = ((String) tableModel.getValueAt(state, 0)).split("");
                    
                // checks the presence of "-" character, which denotes the state as start state
                if (stateString[1].equals("-")) {

                    // the detected starting state will be designated as the first current state for the next part
                    // the row index of the start state is stored in this variable
                    startState = state;
                    break;
                    
                }

            }

        }

        return startState;
    }

    // Method for finding the row index next state, refering to the constructed DFA table
    private int findState(String nextState) {
        
        // initializing variable/s
        int nextcurrentState = 0;

        // go through each of the listed states on the first column and find the next state
        for (int state = 0; state < tableModel.getRowCount(); state++) {

            // retrieves object value of set row and column on the DFA table created and turn into string
            // string is then split per character
            String[] stateString = ((String) tableModel.getValueAt(state, 0)).split("");

            // if nextState and the listed state match, the row index of this state is accessed
            // else, continue
            if(nextState.equals(stateString[0])) {
                nextcurrentState = state;
            }

        }
        
        return nextcurrentState; //returns next currentState row index

    }

    // Method to use to see if current state is final state
    private boolean if_FinalState (int currentState) {

        // state name of row index currentState column index 0 is accessed (the state being checked)
        String current = (String) tableModel.getValueAt(currentState, 0);

        // presence of "+" character denotes state being final state
        if (current.contains("+")) {
            return true;
        }

        // else
        return false;
    }

    private void status(boolean isSuccess, String fileType) {
        statusPanel.removeAll();
        JLabel okLabel = new JLabel();
        okLabel.setName("okLabel");

        //JLabel UI
        okLabel.setFont(customFont);
    
        if (isSuccess) {
            if (fileType.equals(".in") || fileType.equals(".dfa")){
                okLabel.setText("Status: SUCCESS loading " + fileType);
            
            }
            else if (fileType.equals("output")){
                okLabel.setText("Status: Results have been saved to " + outputFileName + "'.");
            }
            okLabel.setForeground(Color.BLACK); // Set text color to green for success
        } else {
            if (fileType.equals(".in") || fileType.equals(".dfa")){
                okLabel.setText("Status: ERROR loading " + fileType);
            
            }
            else if (fileType.equals("output")){
                okLabel.setText("Status: Error saving results to " + outputFileName + "'.");
            }
        }

        // Debugging information
        System.out.println("Adding label to Panel");
        
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
                PE01_CagayDuriasTanjay fileLoader = new PE01_CagayDuriasTanjay();
                fileLoader.setVisible(true);
            }
        });
    }
}
