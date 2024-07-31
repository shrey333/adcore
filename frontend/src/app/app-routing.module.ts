import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CourseListComponent } from './course/course-list/course-list.component';
import { CourseFormComponent } from './course/course-form/course-form.component';

const routes: Routes = [
  { path: '', component: CourseListComponent },
  { path: 'course/new', component: CourseFormComponent },
  { path: 'course/edit/:id', component: CourseFormComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
