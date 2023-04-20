# Anomaly Judgement GUI


Anomaly-judgement-GUI is a graphical user interface built using the Dash framework in Python. It presents suspected abnormal data points to the user, providing all the relevant information needed for the judgement process. The user can then determine whether the data point is abnormal or not, and the result is automatically written to an Excel file.

<br /> 

## Advantages\:

* Intuitive and user-friendly interface
Clear and concise presentation of data points
* Automated Excel file writing, reducing the risk of human error
* Navigation buttons for easy movement between data points
* Input fields and radio buttons for user judgement, with automatic enable/disable logic based on user input

<br /> 

## Concrete Features:

* Interactive plot indicating the anomaly point with a slidebar on x-axis for the feature selected by the user

* Combined plot containing subplots of times series for all features

* Datatable showing all the relevant knowledge point for the p2p lending platform, with filter options for "first-class" and "second-class"

* Text area showing relevant information about the suspected anomaly point and the basic information about the p2p lending platform in which the data anomaly is reported

<br /> 

## Usage instructions

### Run Anomaly Judgement GUI on local Server
1. Run the script `app.py`.
2. Wait for the link to appear in the console
3. Go to the given link using a internet browser

![Running the server](https://user-images.githubusercontent.com/100378969/233264826-085fa3a3-031d-4983-917d-52d76f30202c.png)


### Safely quit and shutdown the server
1. Click the "save and quit" button on the webpage
2. Click "confirm" on the poped up window
3. Close the webpage
4. Enter `Ctrl+C` in the terminal that the server is running

![Shutting down the server](https://user-images.githubusercontent.com/100378969/233264944-0c75d4b9-3530-4de2-8b4e-0ca63972ccfd.png)

<br /> 

## Example screenshots
* Interactive time series plot with slidable plotting window

![Single series plot](https://user-images.githubusercontent.com/100378969/233266302-216ba2a1-66af-4f0c-81b6-63c19dd166f0.png)

<br /> 

* Interactive combination plot with multiple time series

![Multiple series plot](https://user-images.githubusercontent.com/100378969/233266322-5d583482-673c-4989-a978-068189b16407.png)

<br /> 

* Basic infomation plot for peer-to-peer lending platforms

![Basic info plot](https://user-images.githubusercontent.com/100378969/233266821-060e1320-9b11-4679-b154-69ac07cbaed8.png)

