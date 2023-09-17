import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;

public class FileLoaderGUI extends JFrame {
    private JTextArea inputTextArea;
    private JTable dfaTable;
    private DefaultTableModel tableModel;
    private JTextArea outputTextArea;

    public FileLoaderGUI() {
        setTitle("File Loader");
        setSize(800, 600); // Adjusted the initial size
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create a panel for the main content with GridBagLayout
        JPanel mainPanel = new JPanel(new GridBagLayout());
        // Set the background color of the JFrame (the entire window) to pink
        getContentPane().setBackground(Color.PINK);

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.BOTH; // Allow components to grow both horizontally and vertically
        gbc.weightx = 1.0; // Make components take up available horizontal space

        // Create a panel for the buttons
        JPanel buttonPanel = new JPanel();
        JButton loadButton = new JButton("Load Files");
        loadButton.addActionListener(e -> loadFiles());
        JButton processButton = new JButton("Process");
        processButton.addActionListener(e -> processFiles());
        buttonPanel.add(loadButton);
        buttonPanel.add(processButton);
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 3; // Span the buttons across all columns
        mainPanel.add(buttonPanel, gbc); // Put buttons above the UI

       // Create a panel for the Input label and its placeholder
       JPanel inputPanel = new JPanel(new BorderLayout());
       JLabel inputLabel = new JLabel("Input:");
       inputPanel.add(inputLabel, BorderLayout.NORTH);
       inputTextArea = new JTextArea(10, 40);
       JScrollPane inputScrollPane = new JScrollPane(inputTextArea);
       inputPanel.add(inputScrollPane, BorderLayout.CENTER);
       inputPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
       gbc.gridx = 1;
       gbc.gridy = 1;
       gbc.gridwidth = 1;
       gbc.weighty = 2.0; // Increase weighty value for more vertical space
       mainPanel.add(inputPanel, gbc); // Put Input panel on the left

       // Create a panel for the Transition table label and its placeholder
       JPanel dfaPanel = new JPanel(new BorderLayout());
       JLabel dfaLabel = new JLabel("Transition table:");
       dfaPanel.add(dfaLabel, BorderLayout.NORTH);
       tableModel = new DefaultTableModel();
       dfaTable = new JTable(tableModel);
       JScrollPane dfaScrollPane = new JScrollPane(dfaTable);
       dfaPanel.add(dfaScrollPane, BorderLayout.CENTER);
       dfaPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
       gbc.gridx = 0;
       gbc.gridy = 1;
       gbc.weighty = 2.0; // Increase weighty value for more vertical space
       mainPanel.add(dfaPanel, gbc); // Put Transition table panel in the center

       // Create a panel for the Output label and its placeholder
       JPanel outputPanel = new JPanel(new BorderLayout());
       JLabel outputLabel = new JLabel("Output:");
       outputPanel.add(outputLabel, BorderLayout.NORTH);
       outputTextArea = new JTextArea(10, 40);
       JScrollPane outputScrollPane = new JScrollPane(outputTextArea);
       outputPanel.add(outputScrollPane, BorderLayout.CENTER);
       outputPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10)); // Add padding
       gbc.gridx = 2;
       gbc.gridy = 1;
       gbc.weighty = 2.0; // Increase weighty value for more vertical space
       mainPanel.add(outputPanel, gbc); // Put Output panel on the right

       // Add an empty panel to fill remaining vertical space
       JPanel emptyPanel = new JPanel();
       gbc.gridx = 0;
       gbc.gridy = 2;
       gbc.gridwidth = 3;
       gbc.weighty = 1.0; // Make the empty panel take up available vertical space
       mainPanel.add(emptyPanel, gbc);

       // Add the main content to the frame
       add(mainPanel, BorderLayout.CENTER);
   }


    // Method for loading files
    private void loadFiles() {
        JFileChooser fileChooser = new JFileChooser(); // Create a file chooser dialog
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
                } else if (fileName.endsWith(".dfa")) { // If the file has a .dfa extension
                    processDFAFile(content.toString()); // Process and display the .dfa file
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
        outputTextArea.setText(inputTextArea.getText());
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
