function send()
{
//�������� ���������
var data = $('#mydata').val()
  // �������� �������
       $.ajax({
                type: "POST",
                url: "SendData.php",
                data: "data="+data,
                // ������� �� ��� ������ PHP
                success: function(html) {
 //�������������� ������� ������ ������� ��������
                        $("#result").empty();
//� ������� ����� php �������
                        $("#result").append(html);
                }
        });

}