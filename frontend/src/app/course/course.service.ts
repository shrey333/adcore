import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Course } from './course.model';

@Injectable({
  providedIn: 'root',
})
export class CourseService {
  private apiUrl = `https://1a6a-64-189-4-230.ngrok-free.app/api/courses`;
  private headers = new HttpHeaders({
    'ngrok-skip-browser-warning': 'true', // Add the header here
  });

  constructor(private http: HttpClient) {}

  getCourses(
    search: string = '',
    page: number = 1,
    size: number = 10,
  ): Observable<any> {
    return this.http
      .get<any>(`${this.apiUrl}?search=${search}&page=${page}&size=${size}`, {
        headers: this.headers,
      })
      .pipe(
        map((response) => ({
          ...response,
          courses: response.courses.map((course: any) => ({
            ...course,
            StartDate: new Date(course.StartDate),
            EndDate: new Date(course.EndDate),
          })),
        })),
      );
  }

  getCourseById(id: string): Observable<Course> {
    return this.http
      .get<Course>(`${this.apiUrl}/${id}`, { headers: this.headers })
      .pipe(
        map((course) => ({
          ...course,
          StartDate: new Date(course.StartDate),
          EndDate: new Date(course.EndDate),
        })),
      );
  }

  createCourse(course: Course): Observable<string> {
    return this.http.post<string>(`${this.apiUrl}`, course, {
      headers: this.headers,
    });
  }

  updateCourse(id: string, course: Course): Observable<Course> {
    return this.http.put<Course>(`${this.apiUrl}/${id}`, course, {
      headers: this.headers,
    });
  }

  deleteCourse(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`, {
      headers: this.headers,
    });
  }
}
