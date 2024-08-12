import React, {Component} from 'react';
import api from '../../../services/api';

import '../styles.css';

export default class Students extends Component {
  state = {
    students: [],
  };

  async componentDidMount() {
    const response = await api.get(`/students`);

    this.setState({ students: response.data });
  }

  render() {
    return (
      <div className="students-info">
        {this.state.students.map((student) => (
          <article key={student.id}>
            <strong>{student.name}</strong>
            <p>Id: {student.id}</p>
            <p>CPF: {student.cpf}</p>
            <p>RG: {student.rg}</p>
            <p>Idade: {student.age}</p>
            <p>Curso: {student.course}</p>
            <p>Instituição: {student.school.name}</p>
          </article>
        ))}
      </div>
    );
  }
}