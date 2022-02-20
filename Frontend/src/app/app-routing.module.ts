import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {RegisterComponent} from "./register/register.component";
import {MainComponent} from "./main/main.component";
import {UploadMainComponent} from "./upload-main/upload-main.component";
import {TasksComponent} from "./tasks/tasks.component";
import {OverviewComponent} from "./overview/overview.component";

const routes: Routes = [
  {path: '', component: MainComponent},
  {path: 'upload', component: UploadMainComponent},
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'tasks', component: TasksComponent},
  {path: 'overview', component: OverviewComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
