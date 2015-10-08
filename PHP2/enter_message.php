<?php require "header.php"; 
session_start();

// if there is anything in the session field, we'll display it as an error.
if (!empty($_SESSION['message_error']) or strlen($_SESSION['message_error']) > 0) {
  echo $_SESSION['message_error'];
}

function writeFormField($id, $label, $type) {
  echo "<label for=\"$id\">$label</label><br>";
  if ($type == 'text') {
    echo "<input type=\"text\" name=\"$id\" id=\"$id\" required=\"true\">";
  } else if ($type == 'textarea') {
    echo "<textarea id=\"$id\" name=\"$id\"></textarea>";
  }
  echo "<br><br><br>";
}

?>

<h1>Enter a message, person!</h1>
<form method="post" action="submit_message.php">

<?php 
writeFormField('name', 'Name: ', 'text');
writeFormField('subject', 'Subject: ', 'text');
writeFormField('text', 'Text: ', 'textarea');
?>

<input type="submit">
</form>
<br><a href="show_messages.php">back to message list</a>
<?php require "footer.php"; ?>