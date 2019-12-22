function checkInputs(){
    for(input in document.querySelectorAll('input')) {
        if(document.querySelectorAll('input')[input].value === ''){
            document.querySelector('.error_message').textContent = 'Input fields cannot be left blank!'
            return false
        }
    }
    return true
}

function convertJSON(json_object){
    console.log(json_object)
    while(json_object.includes("&#34;")){
        json_object = json_object.replace("&#34;", '"')
    }
    return JSON.parse(json_object)
}

function loadClassrooms(classrooms){
    classrooms_json = convertJSON(classrooms)

    for (classroom in classrooms_json) {
        let newButton = document.createElement('button')
        newButton.textContent = classrooms_json[classroom].class_code + ': ' + classrooms_json[classroom].num_students + ' students'
        newButton.type = 'submit'
        newButton.className = 'classbuttons'
        newButton.name = 'classroom'
        newButton.value = classrooms_json[classroom].class_code
        document.querySelector('.classes form').appendChild(newButton)
    }
}

function loadClassList(classlist){
    classlist_json = convertJSON(classlist)

    for (student in classlist_json) {
        let studentDiv = document.createElement('div')
        studentDiv.className = 'student'

        let studentName = document.createElement('label')
        studentName.textContent = classlist_json[student].first + ' ' + classlist_json[student].last + ' (' + classlist_json[student].id + ')'

        let removeStudent = document.createElement('button')
        removeStudent.name = 'student'
        removeStudent.value = classlist_json[student].id
        removeStudent.className = 'removeStudent'
        removeStudent.textContent = '-'
        removeStudent.type = 'submit'

        studentDiv.appendChild(studentName)
        studentDiv.appendChild(removeStudent)
        document.querySelector('.studentList').appendChild(studentDiv)
    }
}

function findClassCode(){
    let classCode = window.location.pathname.substring(1)
    document.querySelector('title').textContent += classCode
    document.querySelector('.navbar label').textContent += classCode
}