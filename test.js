var fs = require('fs');

function test_reading(file_name)
{
   
    fs.readFile(file_name, {encoding: 'utf-8'}, function(err,data){
        if (!err) {
            console.log('received data: ' + data);
            var tmp = data.split(',');
            var stone_count = (tmp.length-1)/3;
            var state = new Array(stone_count);
            for(i = 0 ; i<stone_count;i++)
            {   state[i] = new Array(3);
                for(j = 3*i ; j<3*i+3; j++)
                {
                    state[i][j/3] = parseInt(tmp[j], 10);;  
                    console.log(tmp[j]);
                }
            }
            //call gui function here.


        } else {
            console.log(err);
        }
    })
}

test_reading('myfile.txt');