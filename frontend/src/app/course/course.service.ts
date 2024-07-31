import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Course } from './course.model';

@Injectable({
  providedIn: 'root',
})
export class CourseService {
  private apiUrl = `http://localhost:8000/api/courses`;

  constructor(private http: HttpClient) {}

  getCourses(
    search: string = '',
    page: number = 1,
    size: number = 10
  ): Observable<any> {
    return this.http
      .get<any>(`${this.apiUrl}?search=${search}&page=${page}&size=${size}`)
      .pipe(
        map((response) => ({
          ...response,
          courses: response.courses.map((course: any) => ({
            ...course,
            StartDate: new Date(course.StartDate),
            EndDate: new Date(course.EndDate),
          })),
        }))
      );
  }

  getCourseById(id: string): Observable<Course> {
    return this.http.get<Course>(`${this.apiUrl}/${id}`).pipe(
      map((course) => ({
        ...course,
        StartDate: new Date(course.StartDate),
        EndDate: new Date(course.EndDate),
      }))
    );
  }

  createCourse(course: Course): Observable<string> {
    return this.http.post<string>(`${this.apiUrl}`, course);
  }

  updateCourse(id: string, course: Course): Observable<Course> {
    return this.http.put<Course>(`${this.apiUrl}/${id}`, course);
  }

  deleteCourse(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}
