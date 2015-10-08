<?php require "header.php"; 

// let's establish a connection.
$conn = new mysqli("localhost", "", "", "test");
if ($conn->connect_error) {
  echo "There is a problem connecting to DB guy (or girl).";
} else {

  // once we've connected we'll retrieve the data from the DB.
  $sql = "SELECT c_name, c_subject, c_time, c_text FROM t_messages";
  $result = $conn->query($sql);
  
  // the num_rows property identifies how many records were returned by the query.
  if ($result->num_rows > 0) {
  
    // for each result, we'll need to retrieve the underlying values.
    // when there are no more records, this will return null.
    while ($row = $result->fetch_assoc()) {
    
      // we'll build some HTML out of the record.
      echo "Name: " . $row['c_name'] . "<br>";
      echo "Subject: " . $row['c_subject'] . "<br>";
      
      // this will format the time.
      $mytime = date('Y-m-d G:m', $row['c_time']);
      echo "Time Posted: $mytime<br>";
      echo "Message:<br>";
      echo $row['c_text'];
      echo "<br><br><br>";
    }
  } else {
    echo "There are no results.";
  }
}

$conn->close();

?>
<a href="enter_message.php">post a new message</a>
<?php require "footer.php"; ?>